import subprocess

import requests
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from app_src.api.models import Admin, Agent, Center, Manager, User


class Reset(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        if settings.LOCAL:

            User.objects.all().delete()
            Admin.objects.all().delete()
            Center.objects.all().delete()
            Manager.objects.all().delete()
            Agent.objects.all().delete()

            data = {
                "username": "admin_username",
                "password": "p",
                "email": "admin@mail.com",
            }
            user = User.objects.create_superuser(**data)
            user.is_admin = True
            user.save()
            admin = Admin.objects.create(user=user)
        return Response({})


class PullAndUpdate(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        subprocess.run(["bash", "update.bash"])

        username = settings.PA_USERNAME
        domain_name = settings.PA_DOMAIN_NAME
        token = settings.PA_TOKEN

        if username and domain_name and token:
            response = requests.post(
                "https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/".format(
                    username=username, domain_name=domain_name
                ),
                headers={"Authorization": "Token {token}".format(token=token)},
            )
            if response.status_code == 200:
                print("Relode info:")
                message = response.json()
            else:
                message = "Got unexpected status code {}: {!r}".format(
                    response.status_code, response.content
                )
            print(message)

        print(
            "https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/".format(
                username=username, domain_name=domain_name
            )
        )
        return Response(message)
