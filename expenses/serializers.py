from rest_framework import serializers

from .models import Expense, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "user",
            "title",
            "amount",
            "date",
            "category",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be positive.")
        return value
