from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from core.permissions import IsViewerOrAbove
from core.responses import success_response
from dashboard.serializers import DashboardQuerySerializer
from dashboard.services import DashboardService


class DashboardSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsViewerOrAbove]
    throttle_scope = "dashboard"

    @extend_schema(
        summary="Dashboard summary and analytics",
        description=(
            "Returns business-focused dashboard analytics including summary totals, "
            "period comparison, top spending categories, insights, monthly trends, and admin-only user breakdown."
        ),
        parameters=[
            OpenApiParameter(
                name="start_date",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter records from this date (YYYY-MM-DD).",
            ),
            OpenApiParameter(
                name="end_date",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter records up to this date (YYYY-MM-DD).",
            ),
        ],
        examples=[
            OpenApiExample(
                "Monthly dashboard example",
                description="A typical monthly analytics request.",
                value={"start_date": "2026-01-01", "end_date": "2026-01-31"},
                request_only=True,
            ),
            OpenApiExample(
                "Dashboard response example",
                description="Representative response payload.",
                value={
                    "summary": {
                        "total_income": "1200.00",
                        "total_expense": "400.00",
                        "net_balance": "800.00",
                        "transaction_count": 4,
                    },
                    "period_comparison": {
                        "current_period": {"start_date": "2026-01-01", "end_date": "2026-01-31"},
                        "previous_period": {"start_date": "2025-12-01", "end_date": "2025-12-31"},
                    },
                    "top_spending_categories": [{"category": "Food", "total_amount": "250.00"}],
                    "insights": [{"type": "expense_spike", "message": "Expenses are up 25.0% compared with the previous period."}],
                },
                response_only=True,
            ),
        ],
    )
    def get(self, request):
        serializer = DashboardQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = DashboardService.get_summary(request.user, serializer.validated_data)
        return success_response(data)
