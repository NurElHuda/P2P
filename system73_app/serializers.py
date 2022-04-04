from rest_framework import serializers
from .models import Network, Tree, Node


class NetworkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = Network
        fields = [
            "id",
            "name",
        ]


class TreeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = Tree
        fields = [
            "id",
            "name",
            "network",
        ]


class NodeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = Node
        fields = [
            "id",
            "name",
            "host",
            "port",
            "tree",
            "parent",
            "children",
        ]
