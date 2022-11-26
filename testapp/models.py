from django.db import models


class Document(models.Model):
    file = models.CharField(max_length=255)
