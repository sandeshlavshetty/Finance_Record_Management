from __future__ import annotations

from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.constants import ADMIN, ANALYST, EXPENSE, INCOME
from records.models import Record
from users.models import User


class RecordAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email="admin@example.com", password="StrongPass123")
        self.analyst = User.objects.create_user(email="analyst@example.com", password="StrongPass123", role=ANALYST)
        self.client.force_authenticate(self.admin)

    def test_admin_can_create_and_soft_delete_record(self):
        response = self.client.post(
            reverse("records-list"),
            {
                "amount": "1000.00",
                "type": INCOME,
                "category": "Salary",
                "date": "2026-01-01",
                "note": "monthly salary",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        record_id = response.data["data"]["id"]

        delete_response = self.client.delete(reverse("records-detail", args=[record_id]))
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertTrue(Record.all_objects.get(id=record_id).is_deleted)

    def test_analyst_can_view_but_not_create(self):
        self.client.force_authenticate(self.analyst)
        list_response = self.client.get(reverse("records-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        create_response = self.client.post(
            reverse("records-list"),
            {
                "amount": "50.00",
                "type": EXPENSE,
                "category": "Coffee",
                "date": "2026-01-01",
                "note": "client meeting",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_category_and_date(self):
        Record.objects.create(user=self.admin, amount=200, type=INCOME, category="Salary", date=date(2026, 1, 1), note="jan")
        Record.objects.create(user=self.admin, amount=50, type=EXPENSE, category="Food", date=date(2026, 1, 2), note="lunch")
        response = self.client.get(reverse("records-list"), {"category": "Salary", "start_date": "2026-01-01", "end_date": "2026-01-31"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 1)
