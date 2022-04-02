from rest_condition import And, Or
from rest_framework import exceptions, generics, permissions

from app_src.api.models import Manager
from app_src.api.permissions import IsAdminUser, IsManagerUser
from app_src.api.serializers import ManagerSerializer


class ManagerList(generics.ListCreateAPIView):

    permission_classes = (
        And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
    )
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class ManagerDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (
        And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
    )
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    lookup_url_kwarg = "manager_id"

    def get_object(self):
        try:
            obj = Manager.objects.get(pk=self.kwargs["manager_id"])
        except Manager.DoesNotExist:
            raise exceptions.NotFound(detail="Manager not found")
        return obj
