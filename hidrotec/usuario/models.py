from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(max_length=50, blank=False)
    nomeFazenda = models.CharField(max_length=50, blank=False)
    senha = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.nome