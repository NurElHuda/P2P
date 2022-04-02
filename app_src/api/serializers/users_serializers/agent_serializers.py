from rest_framework import serializers

from app_src.api.models import Agent, Center, User, create_user, update_user
from app_src.api.serializers.users_serializers.user_serializers import UserSerializer
from app_src.api.serializers.center_serializers import CenterSerializer
from app_src.api.utils import update_object


class AgentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)
    user = UserSerializer()
    center = serializers.PrimaryKeyRelatedField(queryset=Center.objects.all())
    center_verbose = CenterSerializer(source="center", required=False, read_only=True)

    class Meta:
        model = Agent
        fields = ["id", "user", "center", "center_verbose"]
        read_only_fields = ["center_verbose"]

    def create(self, validated_data):
        user = create_user(validated_data.pop("user"))
        agent = Agent.objects.create(user=user, **validated_data)
        return agent

    def update(self, instance, validated_data):
        user_validated_date = validated_data.pop("user", None)
        if user_validated_date:
            instance.user = update_user(instance.user, user_validated_date)
            instance.save()
        instance = update_object(instance, validated_data)
        return instance
