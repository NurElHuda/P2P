from django.test import TestCase
import requests

from p2p_app.models import Network
from django.utils.crypto import get_random_string



class JoinNodeTestCase(TestCase):
    def setUp(self):
        Network.objects.create(name=f"Network {get_random_string(8)}")

    def test_node_can_join(self):
        """
            Join a node to a network
            Test that the node's tree is as expected
            Test that the node's network is as expected
            Test that the node's attribute is as expected
        """
        network = Network.objects.all().order_by("-pk").last()

        node_data = {
            "name": f"N-{get_random_string(8)}",
            "host": "127.0.0.1",
            "port": "0001",
            "capacity": 1,
        }
        res = requests.post(f"127.0.0.1:8000/networks/{network.pk}/connection/")
        assert res.status_code == 201
