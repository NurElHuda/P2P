from rest_condition import And, Or
from rest_framework import exceptions, generics, permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser

from app_src.api.models import Agent, Center, Manager
from app_src.api.permissions import IsAdminUser, IsAgentUser, IsManagerUser
from app_src.api.serializers import (
    AgentSerializer,
    CenterLogoSerializer,
    CenterSerializer,
    ManagerSerializer,
)


class CenterList(generics.ListCreateAPIView):

    permission_classes = (
        And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
    )
    queryset = Center.objects.all()
    serializer_class = CenterSerializer


class CenterDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
    )
    queryset = Center.objects.all()
    lookup_url_kwarg = "center_id"

    def get_object(self):
        try:
            obj = Center.objects.get(pk=self.kwargs["center_id"])
        except Center.DoesNotExist:
            raise exceptions.NotFound(detail="Center not found")
        return obj

    serializer_class = CenterSerializer


class CenterLogo(generics.RetrieveUpdateAPIView):
    permission_classes = (Or(Or(IsAgentUser, IsManagerUser), IsAdminUser),)
    lookup_url_kwarg = "center_id"

    def get_object(self):
        try:
            center = Center.objects.get(pk=self.kwargs["center_id"])
        except Center.DoesNotExist:
            raise exceptions.NotFound(detail="Center not found")
        return center

    serializer_class = CenterLogoSerializer
    parser_classes = [MultiPartParser, FileUploadParser]


class CenterManagerList(generics.ListAPIView):

    permission_classes = (
        And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
    )
    lookup_url_kwarg = "center_id"

    def get_queryset(self):
        return Manager.objects.filter(center__pk=self.kwargs["center_id"])

    serializer_class = ManagerSerializer


class CenterAgentList(generics.ListAPIView):

    permission_classes = (
        And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
    )
    lookup_url_kwarg = "center_id"

    def get_queryset(self):
        return Agent.objects.filter(center__pk=self.kwargs["center_id"])

    serializer_class = AgentSerializer


# class CenterTeacherList(generics.ListAPIView):

#     permission_classes = (
#         And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
#     )
#     lookup_url_kwarg = "center_id"

#     def get_queryset(self):
#         return Teacher.objects.filter(center__pk=self.kwargs["center_id"])

#     serializer_class = TeacherSerializer


# class CenterStudentList(generics.ListAPIView):

#     permission_classes = (
#         And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
#     )
#     lookup_url_kwarg = "center_id"

#     def get_queryset(self):
#         return Student.objects.filter(center__pk=self.kwargs["center_id"])

#     serializer_class = StudentSerializer


# class CenterSessionList(generics.ListAPIView):

#     permission_classes = (
#         And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
#     )
#     lookup_url_kwarg = "center_id"

#     def get_queryset(self):
#         return Session.objects.filter(center__pk=self.kwargs["center_id"])

#     serializer_class = SessionSerializer


# class CenterCourseList(generics.ListAPIView):

#     permission_classes = (
#         And(permissions.IsAuthenticated, Or(IsManagerUser, IsAdminUser)),
#     )
#     lookup_url_kwarg = "center_id"

#     def get_queryset(self):
#         return Course.objects.filter(center__pk=self.kwargs["center_id"])

#     serializer_class = CourseSerializer
