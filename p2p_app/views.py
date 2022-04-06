from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Network, Tree, Node
from .serializers import NetworkSerializer, TreeSerializer, NodeSerializer,NodeConnectSerializer


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

    serializer_class = NodeConnectSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"network_id": self.kwargs.get("network_id")})
        return context


class NetworkConnectionDestroy(APIView):
    def delete(self, request, *args, **kwargs):
        # 1. delete the node
        node = get_object_or_404(Node, pk=self.kwargs['node_id'])
        tree = node.tree
        network = node.network

        # Set the parent of this node as the parent of its children
        children = node.children.all()
        node.parent.children.add(*children)

        # Delete the node
        node.delete()


        # 2. reaarrange the rest of the nodes inside that tree
        tree.rearrange()

        return Response({}, status=204)


class TreeList(generics.ListCreateAPIView):


    queryset = Tree.objects.all()
    serializer_class = TreeSerializer


class NodeList(generics.ListCreateAPIView):


    queryset = Node.objects.all()
    serializer_class = NodeSerializer
