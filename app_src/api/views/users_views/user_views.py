from rest_condition import And, Or
from rest_framework import exceptions, generics, permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAdminUser

from app_src.api.models import User
from app_src.api.permissions import IsAdminUser, IsAgentUser, IsManagerUser
from app_src.api.serializers import UserPictureSerializer, UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (And(permissions.IsAuthenticated, IsAdminUser),)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "user_id"

    def get_object(self):
        try:
            user = User.objects.get(pk=self.kwargs["user_id"])
        except User.DoesNotExist:
            raise exceptions.NotFound(detail="User not found")
        return user

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserCurrent(generics.RetrieveAPIView):
    permission_classes = (Or(Or(IsAgentUser, IsManagerUser), IsAdminUser),)

    def get_object(self):
        try:
            user = User.objects.get(pk=self.request.user.pk)
        except User.DoesNotExist:
            raise exceptions.NotFound(detail="User not found")
        return user

    serializer_class = UserSerializer


class UserPicture(generics.RetrieveUpdateAPIView):
    permission_classes = (Or(Or(IsAgentUser, IsManagerUser), IsAdminUser),)
    lookup_url_kwarg = "user_id"

    def get_object(self):
        try:
            user = User.objects.get(pk=self.kwargs["user_id"])
        except User.DoesNotExist:
            raise exceptions.NotFound(detail="User not found")
        return user

    serializer_class = UserPictureSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
