from __future__ import annotations

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from core.constants import TRANSACTION_TYPE_CHOICES


class RecordQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)


class Record(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="records")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    type = models.CharField(max_length=16, choices=TRANSACTION_TYPE_CHOICES, db_index=True)
    category = models.CharField(max_length=100, db_index=True)
    date = models.DateField(db_index=True)
    note = models.TextField(blank=True, default="")
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = RecordQuerySet.as_manager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["category", "type"]),
            models.Index(fields=["is_deleted", "date"]),
        ]
        constraints = [
            models.CheckConstraint(check=Q(amount__gt=0), name="record_amount_positive"),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} {self.type} {self.amount}"
