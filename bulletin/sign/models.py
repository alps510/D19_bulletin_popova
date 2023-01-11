from django.contrib.auth.models import User
from django.db import models


class OneTimeCode(models.Model):
    code = models.CharField(max_length=5)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
