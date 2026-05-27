from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Workshop, Booking

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class WorkshopSerializer(serializers.ModelSerializer):
    booked_count = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)

    class Meta:
        model = Workshop
        fields = [
            "id",
            "title",
            "description",
            "date",
            "capacity",
            "booked_count",
            "is_full",
            "created_at",
            "updated_at",
        ]


class BookingSerializer(serializers.ModelSerializer):
    workshop = WorkshopSerializer(read_only=True)
    workshop_id = serializers.PrimaryKeyRelatedField(
        queryset=Workshop.objects.all(), write_only=True, source="workshop"
    )

    class Meta:
        model = Booking
        fields = ["id", "user", "workshop", "workshop_id", "created_at"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
