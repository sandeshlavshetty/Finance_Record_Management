from django.urls import path

from dashboard.views import DashboardSummaryAPIView

urlpatterns = [
    path("summary/", DashboardSummaryAPIView.as_view(), name="dashboard-summary"),
]
