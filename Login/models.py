from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=258, primary_key=True)
    password = models.CharField(max_length=258)
    role = models.CharField(max_length=10)
    read_permission = models.BooleanField(default=False)
    write_permission = models.BooleanField(default=False)
    change_permission = models.BooleanField(default=False)

    def __str__(self):
        return self.username
