from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()

PERSON_REGISTER_URL = reverse("persons:register")
PERSON_MANAGE_URL = reverse("persons:manage")
PERSON_LIST_URL = reverse("persons:person-list")

DEFAULT_USER_DATA = {
    "email": "testuser@example.com",
    "password": "testpassword123",
    "first_name": "John",
    "last_name": "Doe"
}
DEFAULT_USER_DATA_TWO = {
    "email": "testuser2@example.com",
    "password": "testpasswordWto1",
    "first_name": "Ann",
    "last_name": "Red"
}
USER_UPDATE_DATA = {
    "email": "updateduser@example.com",
    "first_name": "Updated",
    "last_name": "Name"
}
USER_PARTIAL_UPDATE_DATA = {
    "first_name": "PartialUpdate",
}
DEFAULT_SUPERUSER_DATA = {
    "email": "admin@example.com",
    "password": "adminpassword123",
    "first_name": "Admin",
    "last_name": "User",
    "is_superuser": True,
    "is_staff": True
}


def sample_user(**params):
    defaults = DEFAULT_USER_DATA.copy()
    defaults.update(params)

    return User.objects.create_user(**defaults)


def sample_superuser(**params):
    defaults = DEFAULT_SUPERUSER_DATA.copy()
    defaults.update(params)

    return User.objects.create_superuser(**defaults)


class UnauthenticatedPersonApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_registration_without_authentication(self):
        response = self.client.post(PERSON_REGISTER_URL, DEFAULT_USER_DATA)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthenticatedPersonApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.detail_url = reverse("persons:manage")

    def test_retrieve_authenticated_person_details(self):
        response = self.client.get(PERSON_MANAGE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_standard_user_restricted_access_to_person_list(self):
        response = self.client.get(PERSON_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_update_own_details(self):
        response = self.client.put(self.detail_url, USER_UPDATE_DATA)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        for key, value in USER_UPDATE_DATA.items():
            if key != "password":
                self.assertEqual(getattr(self.user, key), value)

    def test_authenticated_user_can_partially_update_own_details(self):
        response = self.client.patch(self.detail_url, USER_PARTIAL_UPDATE_DATA)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        for key, value in USER_PARTIAL_UPDATE_DATA.items():
            self.assertEqual(getattr(self.user, key), value)

    def test_authenticated_user_can_delete_own_account(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class AdminPersonApiTests(TestCase):

    @staticmethod
    def person_detail_url(user_id) -> str:
        return reverse("persons:person-detail", args=[user_id])

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = sample_user()
        cls.superuser = sample_superuser()

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(self.superuser)

    def test_admin_granted_access_to_person_list(self):
        response = self.client.get(PERSON_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_any_person(self):
        url = self.person_detail_url(self.user.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_create_person(self):
        response = self.client.post(PERSON_REGISTER_URL, DEFAULT_USER_DATA_TWO)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update_any_person(self):
        url = self.person_detail_url(self.user.id)
        response = self.client.put(url, USER_UPDATE_DATA)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_partially_update_any_person(self):
        url = self.person_detail_url(self.user.id)
        response = self.client.patch(url, USER_PARTIAL_UPDATE_DATA)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
