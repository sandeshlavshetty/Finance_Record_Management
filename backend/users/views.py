from __future__ import annotations

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from core.permissions import IsAdminRole
from core.responses import success_response
from users.models import User
from users.serializers import (
    CustomTokenObtainPairSerializer,
    UserCreateSerializer,
    UserRoleUpdateSerializer,
    UserStatusUpdateSerializer,
    UserSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_scope = "auth"


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    throttle_scope = "users"

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action == "assign_role":
            return UserRoleUpdateSerializer
        if self.action == "set_status":
            return UserStatusUpdateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success_response(UserSerializer(user).data, status_code=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        users = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(users, many=True)
        return success_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        return success_response(UserSerializer(user).data)

    @action(detail=True, methods=["patch"], url_path="role")
    def assign_role(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        return success_response(UserSerializer(updated_user).data)

    @action(detail=True, methods=["patch"], url_path="status")
    def set_status(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        return success_response(UserSerializer(updated_user).data)
