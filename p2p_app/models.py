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
        null=True,
        blank=True
    )


    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f"Tree {self.pk} | {self.name}"

    def rearrange(self):
        leafs = self.nodes.filter(children__lte=0)
        for node in leafs:
            optimal_node = self.objects.exclude(pk=node.pk).filter(freespace__gte=1).order_by("-freespace").first()
            if optimal_node:
                node.parent = optimal_node
                node.save()
                optimal_node.update_freespace()




class Node(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=64)
    port = models.CharField(max_length=64)
    capacity = models.IntegerField(default=0)
    freespace = models.IntegerField(default=0)

    tree = models.ForeignKey(
        "Tree",
        related_name="nodes",
        on_delete=models.CASCADE,
        null=True,
        blank=True
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

    def save(self, *args, **kwargs):
        self.freespace = self.capacity - self.children.all().count()
        return super().save(*args, **kwargs)

    def update_freespace(self):
        self.freespace = self.capacity - self.children.all().count()
        self.save()