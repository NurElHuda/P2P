from django.urls import path

from p2p_app import views

app_name = "p2p_app"


urlpatterns = [
    path(
        "networks/",
        views.NetworkList.as_view(),
        name="network-list",
    ),
    path(
        "networks/<int:network_id>/status/",
        views.NetworkStatus.as_view(),
        name="network-status",
    ),
    path(
        "networks/<int:network_id>/connection/",
        views.NetworkConnectionCreate.as_view(),
        name="network-connection-create",
    ),
    path(
        "networks/<int:network_id>/connection/<int:node_id>/",
        views.NetworkConnectionDestroy.as_view(),
        name="network-connection-destroy",
    ),
    path(
        "trees/",
        views.TreeList.as_view(),
        name="tree-list",
    ),
    path(
        "nodes/",
        views.NodeList.as_view(),
        name="node-list",
    ),
]
