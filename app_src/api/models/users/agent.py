from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_lifecycle import hook
from django_lifecycle.hooks import AFTER_CREATE
from django_lifecycle.mixins import LifecycleModelMixin


class Agent(LifecycleModelMixin, models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    user = models.OneToOneField(
        "api.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="agent",
    )

    center = models.ForeignKey(
        "api.Center",
        on_delete=models.CASCADE,
        related_name="agents",
        null=True,
        default=None,
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        return super(Agent, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("api:agent-detail", kwargs={"id": self.pk})

    @hook(AFTER_CREATE)
    def set_user_type(self):
        self.user.is_agent = True
        self.user.save()
