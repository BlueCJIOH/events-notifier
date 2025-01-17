from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "roles"

    def __str__(self) -> str:
        return self.name
