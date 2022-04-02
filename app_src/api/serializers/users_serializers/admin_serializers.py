from rest_framework import serializers

from app_src.api.models import Admin, User, create_user, update_user
from app_src.api.serializers.users_serializers.user_serializers import UserSerializer


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Admin
        fields = [
            "user",
        ]

    def create(self, validated_data):
        user = create_user(validated_data.pop("user"))
        user.is_admin = True
        admin = Admin.objects.create(user=user, **validated_data)
        return admin

    def update(self, instance, validated_data):
        user_validated_date = validated_data.pop("user", None)
        if user_validated_date:
            instance.user = update_user(instance.user, user_validated_date)
            instance.save()
        return instance
