# from rest_framework import serializers

# from app_src.api.models import Admin, User
# from app_src.api.serializers.user_serializers import UserSerializer


# class AdminSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=True)

#     class Meta:
#         model = Admin
#         fields = [
#             "user",
#         ]

#     def create(self, validated_data):
#         user = UserSerializer(instance=None, data=validated_data.pop("user"))
#         user.is_admin = True
#         admin = Admin.objects.create(user=user, **validated_data)
#         return admin

#     def update(self, instance, validated_data):
#         instance.user = UserSerializer(
#             instance=instance.user, data=validated_data.pop("user")
#         )
#         instance.user.save()
#         return instance
