from rest_framework import serializers

from app_src.api.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)
    password = serializers.CharField(write_only=True)
    picture = serializers.ImageField(
        max_length=1000, allow_empty_file=False, use_url=True, read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "family_name",
            "email",
            "username",
            "gender",
            "password",
            "birthday",
            "picture",
            "user_type",
        ]
        write_only_fields = [
            "password",
        ]


class UserPictureSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
        max_length=5000, allow_empty_file=False, use_url=True
    )

    class Meta:
        model = User
        fields = ["id", "picture"]

    def update(self, instance, validated_data):
        instance.picture = validated_data.get("picture", None)
        instance.save()
        return instance
