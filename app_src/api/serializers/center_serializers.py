from rest_framework import serializers

from app_src.api.models import Center


class CenterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = Center
        fields = [
            "id",
            "name",
            "phone",
            "logo",
            "address",
        ]
        read_only_fields = [
            "logo",
        ]


class CenterLogoSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(max_length=5000, allow_empty_file=False, use_url=True)

    class Meta:
        model = Center
        fields = ["id", "logo"]

    def update(self, instance, validated_data):
        instance.logo = validated_data.get("logo", None)
        instance.save()
        return instance
