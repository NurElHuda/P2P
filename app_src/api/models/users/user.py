from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook
from django_lifecycle.hooks import BEFORE_SAVE
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser, LifecycleModelMixin):

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    USER_TYPE = [
        ("Admin", "Admin"),
        ("Manager", "Manager"),
        ("Staff", "Staff"),
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    ]

    name = models.CharField(_("Name"), blank=True, max_length=255, default="")
    family_name = models.CharField(
        _("Family name"), blank=True, max_length=255, default=""
    )
    gender = models.CharField(_("Gender"), blank=True, max_length=1, default="")
    email = models.EmailField(max_length=255, unique=True)
    birthday = DateField(default=None, null=True, blank=True)
    picture = ProcessedImageField(
        max_length=1000,
        upload_to="users/images",
        processors=[ResizeToFill(413, 531)],
        format="JPEG",
        options={"quality": 85},
        null=True,
    )

    is_admin = models.BooleanField(_("IsAdmin"), default=False)
    is_manager = models.BooleanField(_("IsManager"), default=False)
    is_agent = models.BooleanField(_("IsAgent"), default=False)
    is_teacher = models.BooleanField(_("IsTeacher"), default=False)
    is_student = models.BooleanField(_("IsStudent"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        return super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("api:user-detail", kwargs={"id": self.pk})

    def __str__(self):
        return self.name + " " + self.family_name

    @property
    def user_type(self):
        if self.is_admin:
            return "admin"
        elif self.is_manager:
            return "manager"
        elif self.is_teacher:
            return "teacher"
        elif self.is_student:
            return "student"
        else:
            return "unknown"


def create_user(user_validated_data):
    password = user_validated_data.pop("password", False)
    user = User.objects.create(**user_validated_data)
    user.set_password(password)
    user.save()
    return user


def update_user(user, validated_data):
    user.name = validated_data.get("name", user.name)
    user.email = validated_data.get("email", user.email)
    if validated_data.get("password", False):
        user.set_password(validated_data.get("password"))
    user.username = validated_data.get("username", user.username)
    user.birthday = validated_data.get("birthday", user.birthday)
    user.save()
    return user
