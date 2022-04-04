from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions

from .models import Network, Tree, Node
from .serializers import NetworkSerializer, TreeSerializer, NodeSerializer


class NetworkList(generics.ListCreateAPIView):


    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class NetworkConnectionCreate(generics.CreateAPIView):


    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class NetworkConnectionDestroy(generics.DestroyAPIView):


    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class NetworkStatus(generics.DestroyAPIView):


    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class TreeList(generics.ListCreateAPIView):


    queryset = Tree.objects.all()
    serializer_class = TreeSerializer


class NodeList(generics.ListCreateAPIView):


    queryset = Node.objects.all()
    serializer_class = NodeSerializer
