from __future__ import annotations

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdminRole, IsAnalystOrAdmin
from core.responses import success_response
from records.filters import RecordFilter
from records.models import Record
from records.serializers import RecordSerializer, RecordWriteSerializer
from records.services import RecordService


@extend_schema_view(
    create=extend_schema(tags=["Records"], summary="Create record"),
    list=extend_schema(tags=["Records"], summary="List records"),
    retrieve=extend_schema(tags=["Records"], summary="Get record"),
    update=extend_schema(tags=["Records"], summary="Update record"),
    partial_update=extend_schema(tags=["Records"], summary="Partially update record"),
    destroy=extend_schema(tags=["Records"], summary="Delete record"),
)
class RecordViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Record.objects.select_related("user").active()
    filterset_class = RecordFilter
    search_fields = ["note", "category"]
    ordering_fields = ["date", "created_at", "amount"]
    throttle_scope = "records"

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            permission_classes = [IsAuthenticated, IsAdminRole]
        else:
            permission_classes = [IsAuthenticated, IsAnalystOrAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            return RecordWriteSerializer
        return RecordSerializer

    def get_queryset(self):
        return RecordService.build_queryset(self.request.user, self.request.query_params)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RecordSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RecordSerializer(queryset, many=True)
        return success_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        record = self.get_object()
        return success_response(RecordSerializer(record).data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        return success_response(RecordSerializer(record).data, status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        serializer = self.get_serializer(record, data=request.data, partial=kwargs.get("partial", False), context={"request": request})
        serializer.is_valid(raise_exception=True)
        updated_record = serializer.save()
        return success_response(RecordSerializer(updated_record).data)

    def destroy(self, request, *args, **kwargs):
        record = self.get_object()
        RecordService.soft_delete_record(record)
        return success_response({"deleted": True})
