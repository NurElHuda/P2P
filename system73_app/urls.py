from django.urls import path

from system73_app import views

app_name = "system73_app"


urlpatterns = [
    path(
        "networks/",
        views.NetworkList.as_view(),
        name="network-list",
    ),
    path(
        "networks/<network_id:int>/status/",
        views.NetworkStatus.as_view(),
        name="network-status",
    ),
    path(
        "networks/<network_id:int>/connection/",
        views.NetworkConnectionCreate.as_view(),
        name="network-connection-create",
    ),
    path(
        "networks/<network_id:int>/connection/<node_id:int>/",
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
