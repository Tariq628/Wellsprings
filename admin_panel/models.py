from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_types", "SA")  # Set the user_type for superuser
        group, _ = Group.objects.get_or_create(name="SA")
        user = self._create_user(username, email, password, **extra_fields)
        user.groups.add(group)
        return user


class Manager(AbstractUser):
    options_for_user_types = (
        ("SA", "Super Admin"),
        ("BM", "Branch Manager"),
        ("CM", "Case Manager"),
        ("client", "Client"),
    )
    user_types = models.CharField(
        max_length=6, blank=True, choices=options_for_user_types
    )
    organisation = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    objects = CustomUserManager()
    is_verified = models.IntegerField(max_length=2, default=0)

    class Meta:
        db_table = "managers"

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.set_password(self.password)
            self.is_staff = True
        super(Manager, self).save(*args, **kwargs)
        print("Manager", self.__dict__)
        if self.user_types == "SA":
            group, _ = Group.objects.get_or_create(name="SA")
            self.groups.add(group)
        elif self.user_types == "BM":
            group, _ = Group.objects.get_or_create(name="BM")
            self.groups.add(group)

        elif self.user_types == "CM":
            group, _ = Group.objects.get_or_create(name="CM")
            self.groups.add(group)
