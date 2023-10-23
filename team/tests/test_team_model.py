from django.contrib.auth import get_user_model
from team.models import Team
from django.test import TestCase


class TeamModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="test12345"
        )

    def test_team_str_representation(self):
        self.client.login(email="admin@example.com", password="test12345")
        team = Team.objects.create(name="TodoTeam")

        self.assertEqual(str(team), f"{team.name}, ID: {team.id}")