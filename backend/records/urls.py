from django.urls import include, path
from rest_framework.routers import DefaultRouter

from records.views import RecordViewSet

router = DefaultRouter()
router.register(r"", RecordViewSet, basename="records")

urlpatterns = [
    path("", include(router.urls)),
]
