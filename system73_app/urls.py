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
