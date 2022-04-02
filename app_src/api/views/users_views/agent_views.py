from rest_condition import Or
from rest_framework import exceptions, generics

from app_src.api.models import Agent
from app_src.api.permissions import IsAdminUser, IsAgentUser, IsManagerUser
from app_src.api.serializers import AgentSerializer


class AgentList(generics.ListCreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = (Or(Or(IsAgentUser, IsManagerUser), IsAdminUser),)


class AgentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = (Or(Or(IsAgentUser, IsManagerUser), IsAdminUser),)
    lookup_url_kwarg = "agent_id"

    def get_object(self):
        try:
            obj = Agent.objects.get(pk=self.kwargs["agent_id"])
        except Agent.DoesNotExist:
            raise exceptions.NotFound(detail="Agent not found")
        return obj
