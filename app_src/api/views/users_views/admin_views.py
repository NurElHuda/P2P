from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from app_src.api.models import Admin
from app_src.api.serializers import AdminSerializer


class AdminList(generics.ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]
