from django.contrib.auth.models import AbstractUser
from django.db import models

from config.base import NULLABLE


class Seat(models.Model):
    """
    Represents the type of license a user can have.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "seats"


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, related_name="users", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"

