from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.constants import ADMIN, ANALYST, VIEWER
from users.models import User


class UserAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email="admin@example.com", password="StrongPass123")
        self.viewer = User.objects.create_user(email="viewer@example.com", password="StrongPass123", role=VIEWER)
        self.client.force_authenticate(self.admin)

    def test_admin_can_create_user(self):
        response = self.client.post(
            reverse("users-list"),
            {"email": "analyst@example.com", "password": "StrongPass123", "role": ANALYST},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["role"], ANALYST)

    def test_admin_can_assign_role(self):
        response = self.client.patch(
            reverse("users-assign-role", args=[self.viewer.id]),
            {"role": ANALYST},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.viewer.refresh_from_db()
        self.assertEqual(self.viewer.role, ANALYST)

    def test_non_admin_is_blocked(self):
        self.client.force_authenticate(self.viewer)
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
