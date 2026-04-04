from __future__ import annotations

from decimal import Decimal

from django.db.models import Case, Count, DecimalField, Sum, Value, When
from django.db.models.functions import TruncMonth

from core.constants import ADMIN, ANALYST, EXPENSE, INCOME, VIEWER
from records.models import Record


class DashboardService:
    @staticmethod
    def _base_queryset(user):
        if user.role not in {ADMIN, ANALYST, VIEWER}:
            return Record.objects.none()
        return Record.objects.active().select_related("user")

    @classmethod
    def get_summary(cls, user, filters):
        queryset = cls._base_queryset(user)
        if filters.get("start_date"):
            queryset = queryset.filter(date__gte=filters["start_date"])
        if filters.get("end_date"):
            queryset = queryset.filter(date__lte=filters["end_date"])

        totals = queryset.aggregate(
            total_income=Sum(Case(When(type=INCOME, then="amount"), default=Value(Decimal("0.00")), output_field=DecimalField(max_digits=12, decimal_places=2))),
            total_expense=Sum(Case(When(type=EXPENSE, then="amount"), default=Value(Decimal("0.00")), output_field=DecimalField(max_digits=12, decimal_places=2))),
        )
        total_income = totals["total_income"] or Decimal("0.00")
        total_expense = totals["total_expense"] or Decimal("0.00")

        category_breakdown = list(
            queryset.values("category").annotate(
                total_amount=Sum("amount"),
                record_count=Count("id"),
            ).order_by("-total_amount", "category")
        )

        recent_transactions = list(
            queryset.order_by("-date", "-created_at").values(
                "id", "amount", "type", "category", "date", "note", "created_at", "user__email"
            )[:5]
        )

        monthly_trends = list(
            queryset.annotate(month=TruncMonth("date")).values("month").annotate(
                income=Sum(Case(When(type=INCOME, then="amount"), default=Value(Decimal("0.00")), output_field=DecimalField(max_digits=12, decimal_places=2))),
                expense=Sum(Case(When(type=EXPENSE, then="amount"), default=Value(Decimal("0.00")), output_field=DecimalField(max_digits=12, decimal_places=2))),
            ).order_by("month")
        )

        return {
            "summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "net_balance": total_income - total_expense,
                "transaction_count": queryset.count(),
            },
            "category_breakdown": category_breakdown,
            "recent_transactions": recent_transactions,
            "monthly_trends": monthly_trends,
        }
