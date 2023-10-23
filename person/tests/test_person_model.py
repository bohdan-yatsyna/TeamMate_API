from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class PersonModelTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="TestPassword1",
            first_name="The",
            last_name="Test",
        )
        self.client.force_authenticate(self.user)

    def test_user_str_representation(self):
        expected_str_representation = (
            f"{self.user.first_name} {self.user.last_name}, id: {self.user.id}"
        )

        self.assertEqual(str(self.user), expected_str_representation)
