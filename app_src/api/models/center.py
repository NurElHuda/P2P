from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Center(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    name = models.CharField(_("Name of center"), max_length=1000, default="")
    address = models.CharField(_("Address of center"), max_length=1000, default="")
    phone = models.CharField(_("Phone of center"), max_length=1000, default="")
    logo = models.ImageField(
        _("Logo of center"), upload_to="centers/logo", null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("centers:detail", kwargs={"id": self.pk})
