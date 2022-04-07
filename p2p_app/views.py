from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import graphviz


from .models import Network, Tree, Node
from .serializers import (
    NetworkSerializer,
    TreeSerializer,
    NodeSerializer,
    NodeConnectSerializer,
)


class NetworkList(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        """
            List all networks
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Create a new network
        """
        return self.create(request, *args, **kwargs)

    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class NetworkConnectionCreate(generics.CreateAPIView):
        """
            Add a node and connect it to the network
        """

        def get_object(self):
            network = get_object_or_404(Node, pk=self.kwargs["network_id"])
            return network

        serializer_class = NodeConnectSerializer

        def get_serializer_context(self):
            context = super().get_serializer_context()
            context.update({"network_id": self.kwargs.get("network_id")})
            return context


class NetworkConnectionDestroy(APIView):
    """
        Disconnect a node from the network, then rearrange its tree as a breath first tree
    """

    def delete(self, request, *args, **kwargs):
        # 1. delete the node
        node = get_object_or_404(Node, pk=self.kwargs["node_id"])
        tree = node.tree
        network = node.tree.network

        # Set the parent of this node as the parent of its children
        children = node.children.all()
        if node.parent:
            node.parent.children.add(*children)
        else:
            children.update(parent=None)

        # Delete the node
        node.delete()

        # 2. reaarrange the rest of the nodes inside that tree
        tree.rearrange()

        return Response({}, status=204)


class NetworkStatus(APIView):
    """
        Return the status of the network in two format:
            1. The topology in JSON GRAPH FORMAT
            2. A graph of the topology in a PNG file.
    """

    def get(self, request, *args, **kwargs):
        network = get_object_or_404(Network, pk=self.kwargs["network_id"])
        trees = network.trees.all()
        nodes = Node.objects.filter(
            tree__in=trees,
        )

        graph = {"graph": {"directed": False, "nodes": {}, "edges": []}}
        dot = graphviz.Graph(network.name, format="png")

        for node in nodes:
            dot.node(str(node.name))
            graph["graph"]["nodes"][str(node.name)] = {}
            if node.parent:
                dot.edge(str(node.parent.name), str(node.name))
                graph["graph"]["edges"] += {"source": str(node.parent.name), "target": str(node.name)},

        filename = get_random_string(8)
        dot.render(filename=filename, directory="p2p_app/media/graphs", cleanup=True).replace("\\", "/")
        return Response({"json_graph_format": graph, "file": f"http://127.0.0.1:8000/media/graphs/{filename}.png"}, status=200)


class TreeList(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        """
            List all trees
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Create a new tree
        """
        return self.create(request, *args, **kwargs)

    queryset = Tree.objects.all()
    serializer_class = TreeSerializer


class NodeList(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        """
            List all nodes
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Create a new node
        """
        return self.create(request, *args, **kwargs)
        
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
