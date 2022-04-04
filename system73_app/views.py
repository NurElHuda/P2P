from ast import Delete
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions

from .models import Network, Tree, Node
from .serializers import NetworkSerializer, TreeSerializer, NodeSerializer


class NetworkList(generics.ListCreateAPIView):


    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class NetworkStatus(generics.RetrieveAPIView):

    def get_object(self):
        network = get_object_or_404(Node, pk=self.kwargs["network_id"])
        return network

    # TODO: setup extensive serializer for point 3.
    serializer_class = NetworkSerializer


class NetworkConnectionCreate(generics.CreateAPIView):

    def get_object(self):
        network = get_object_or_404(Node, pk=self.kwargs["network_id"])
        return network

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    serializer_class = NodeSerializer


class NetworkConnectionDestroy(generics.DestroyAPIView):
    queryset = Network.objects.all()

    def get_object(self):
        node = get_object_or_404(Node, pk=self.kwargs["node_id"])
        return node

    serializer_class = NetworkSerializer


class TreeList(generics.ListCreateAPIView):


    queryset = Tree.objects.all()
    serializer_class = TreeSerializer


class NodeList(generics.ListCreateAPIView):


    queryset = Node.objects.all()
    serializer_class = NodeSerializer
