from django.db import models


class Network(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Network"
        verbose_name_plural = "Networks"

    def __str__(self):
        return f"Network {self.pk} | {self.name}"


class Tree(models.Model):
    name = models.CharField(max_length=100)
    network = models.ForeignKey(
        "Network",
        related_name="trees",
        on_delete=models.CASCADE,
    )


    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f"Tree {self.pk} | {self.name}"


class Node(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=64)
    port = models.CharField(max_length=64)
    capacity = models.CharField(max_length=64)

    tree = models.ForeignKey(
        "Tree",
        related_name="nodes",
        on_delete=models.CASCADE,
    )

    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f"Node {self.pk} | {self.name}"
