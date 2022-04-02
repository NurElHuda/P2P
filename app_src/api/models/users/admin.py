from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Admin(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    user = models.OneToOneField(
        "api.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="admin",
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        else:
            self.user.is_admin = True
        return super(Admin, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("api:admin-detail", kwargs={"id": self.pk})
