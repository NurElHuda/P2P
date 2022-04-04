import re
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
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
            "capacity",
            "freespace",
            "tree",
            "parent",
            "children",
        ]
        read_only_fields = ["freespace"]


class NodeConnectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)
    network = serializers.PrimaryKeyRelatedField(source="tree.network", read_only=True)
    class Meta:
        model = Node
        fields = [
            "id",
            "name",
            "host",
            "port",
            "capacity",
            "tree",
            "network",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        try:
            network = Network.objects.get(pk=self.context["network_id"])
        except Network.DoesNotExist:
            network = Network.objects.create(name=f"N-{get_random_string(8)}")

        attrs["network"] = network
        return attrs

    def create(self, validated_data):
        network = validated_data.pop("network", None)
        instance = Node.objects.create(**validated_data)

        optimal_node = Node.objects.exclude(pk=instance.pk).filter(freespace__gte=1).order_by("freespace").first()
        if optimal_node:
            instance.parent = optimal_node
            instance.tree = optimal_node.tree
            instance.save()
            optimal_node.update_freespace()
        else:
            new_tree = Tree.objects.create(name=f"T-{get_random_string(8)}", network=network)
            new_tree.nodes.add(instance)

        return instance
