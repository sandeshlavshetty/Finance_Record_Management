from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from datetime import date

from core.constants import EXPENSE, INCOME, VIEWER
from records.models import Record
from users.models import User


class DashboardAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email="admin@example.com", password="StrongPass123")
        self.viewer = User.objects.create_user(email="viewer@example.com", password="StrongPass123", role=VIEWER)
        Record.objects.create(user=self.admin, amount=1000, type=INCOME, category="Salary", date=date(2026, 1, 1), note="salary")
        Record.objects.create(user=self.admin, amount=250, type=EXPENSE, category="Food", date=date(2026, 1, 2), note="groceries")

    def test_viewer_can_read_dashboard_summary(self):
        self.client.force_authenticate(self.viewer)
        response = self.client.get(reverse("dashboard-summary"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["summary"]["transaction_count"], 2)

    def test_date_filters_are_validated(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("dashboard-summary"), {"start_date": "2026-02-01", "end_date": "2026-01-01"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
