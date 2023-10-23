from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from person.models import Person
from team.models import Team


class BaseSetup(APITestCase):

    def setUp(self):
        self.admin = Person.objects.create_superuser(
            email="admin@example.com", password="adminQWE123"
        )
        self.user = Person.objects.create_user(
            email="user@example.com", password="userWEVF123"
        )
        self.team = Team.objects.create(name="Team Mate TEST")
        self.team_list_url = reverse("teams:team-list")
        self.team_detail_url = reverse("teams:team-detail", args=[self.team.id])

    def authenticate_with_token(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def get_response_for_user(self, url, method, user, data=None):
        token = str(RefreshToken.for_user(user).access_token)
        self.authenticate_with_token(token)

        if method == "get":
            return self.client.get(url)

        elif method == "post":
            return self.client.post(url, data)

        elif method == "put":
            return self.client.put(url, data)

        elif method == "delete":
            return self.client.delete(url)

        raise f"Unsupported method: {method}"


class TeamsFunctionalityUnauthenticatedUserTests(BaseSetup):

    def test_list_teams_by_unauthenticated_user_denied(self):
        response = self.client.get(self.team_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TeamsFunctionalityRegularUserTests(BaseSetup):

    def test_list_teams_by_standard_user(self):
        response = self.get_response_for_user(self.team_list_url, "get", self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team_by_standard_user_denied(self):
        data = {"name": "Team C"}
        response = self.get_response_for_user(self.team_list_url, "post", self.user, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_team_by_standard_user(self):
        response = self.get_response_for_user(self.team_detail_url, "get", self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_team_by_standard_user_denied(self):
        data = {"name": "Updated Again"}
        response = self.get_response_for_user(self.team_detail_url, "put", self.user, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_team_by_standard_user_denied(self):
        response = self.get_response_for_user(self.team_detail_url, "delete", self.user)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TeamsFunctionalityAdminUserTests(BaseSetup):

    def test_create_team_by_admin(self):
        data = {"name": "Team B"}
        response = self.get_response_for_user(self.team_list_url, "post", self.admin, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_team_by_admin(self):
        data = {"name": "Updated Team"}
        response = self.get_response_for_user(self.team_detail_url, "put", self.admin, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_team_by_admin(self):
        response = self.get_response_for_user(self.team_detail_url, "delete", self.admin)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
