from __future__ import annotations

from rest_framework import serializers

from records.models import Record
from records.services import RecordService


class RecordSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Record
        fields = ["id", "user_email", "amount", "type", "category", "date", "note", "created_at"]
        read_only_fields = ["id", "user_email", "created_at"]


class RecordWriteSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    type = serializers.ChoiceField(choices=[("income", "Income"), ("expense", "Expense")])
    category = serializers.CharField(max_length=100)
    date = serializers.DateField()
    note = serializers.CharField(required=False, allow_blank=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        return RecordService.create_record(self.context["request"].user, validated_data)

    def update(self, instance, validated_data):
        return RecordService.update_record(instance, validated_data)
