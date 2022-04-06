from django.test import TestCase
from rest_framework.test import APIClient
from p2p_app.models import Network, Node
from django.utils.crypto import get_random_string


class JoinNodeTestCase(TestCase):
    def setUp(self):
        Network.objects.create(name=f"Network 1")

    def test_node_join(self):
        """
        Join a node to a network
        Test that the node's tree is as expected
        Test that the node's network is as expected
        Test that the node's attribute is as expected
        """
        client = APIClient()
        network = Network.objects.get(name="Network 1")

        # N1 join the network
        req_node_data = {
            "name": "N1",
            "host": "127.0.0.1",
            "port": "0001",
            "capacity": 5,
        }

        res = client.post(f"/networks/{network.pk}/connection/", req_node_data)
        assert res.status_code == 201

        # Test that the field of the node are as expected.
        res_node_data = res.json()
        field_lists = ["name", "host", "port", "capacity"]
        for field in field_lists:
            assert res_node_data[field] == req_node_data[field]

        # Test that the node has joined the correct network
        assert res_node_data["network"] == network.pk

        # Verify that the node is shown in graph from endpoint /status/
        res_status = client.get(f"/networks/{network.pk}/status/")
        assert res_status.status_code == 200
        res_status_data = res_status.json()
        assert (
            str(res_node_data["id"])
            in res_status_data["json_graph_format"]["graph"]["nodes"]
        )

        # N2 join the network
        req_node_2_data = {
            "name": f"N2",
            "host": "127.0.0.1",
            "port": "0001",
            "capacity": 1,
        }

        res_node_2 = client.post(f"/networks/{network.pk}/connection/", req_node_2_data)
        assert res_node_2.status_code == 201
        res_node_2_data = res_node_2.json()
        # Test that N2 is a child of N1
        assert res_node_2_data["parent"] == res_node_data["id"]

        # N3 join the network
        req_node_3_data = {
            "name": f"N3",
            "host": "127.0.0.1",
            "port": "0001",
            "capacity": 0,
        }

        res_node_3 = client.post(f"/networks/{network.pk}/connection/", req_node_3_data)
        assert res_node_3.status_code == 201
        res_node_3_data = res_node_3.json()
        # Test that N3 is a child of N1: (the node with the most free capacity)
        assert res_node_3_data["parent"] == res_node_data["id"]


class LeaveNodeTestCase(TestCase):
    def setUp(self):
        network = Network.objects.create(name=f"Network 1")
        client = APIClient()
        res_node_1 = client.post(
            f"/networks/{network.pk}/connection/",
            {
                "name": "N1",
                "host": "127.0.0.1",
                "port": "0001",
                "capacity": 1,
            },
        )
        res_node_2 = client.post(
            f"/networks/{network.pk}/connection/",
            {
                "name": "N2",
                "host": "127.0.0.1",
                "port": "0002",
                "capacity": 1,
            },
        )
        res_node_3 = client.post(
            f"/networks/{network.pk}/connection/",
            {
                "name": "N3",
                "host": "127.0.0.1",
                "port": "0003",
                "capacity": 0,
            },
        )

    def test_node_leave(self):
        """
        Disconnect a node from a network
        Test that the node's tree is as expected
        Test that the node's network is as expected
        Test that the node's attribute is as expected
        """
        client = APIClient()
        network = Network.objects.get(name="Network 1")
        node_2 = Node.objects.get(name="N2")


        res = client.get(f"/networks/{network.pk}/status/")
        assert res.status_code == 200

        res = client.delete(f"/networks/{network.pk}/connection/{node_2.pk}/")
        assert res.status_code == 204

        # Verify that N3 became N1's child
        node_1 = Node.objects.get(name="N1")
        node_3 = Node.objects.get(name="N3")
        assert node_3.parent.pk == node_1.pk
