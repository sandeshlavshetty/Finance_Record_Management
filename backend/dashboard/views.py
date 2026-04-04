from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.permissions import IsViewerOrAbove
from core.responses import success_response
from dashboard.serializers import DashboardQuerySerializer
from dashboard.services import DashboardService


class DashboardSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsViewerOrAbove]
    throttle_scope = "dashboard"

    def get(self, request):
        serializer = DashboardQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = DashboardService.get_summary(request.user, serializer.validated_data)
        return success_response(data)
