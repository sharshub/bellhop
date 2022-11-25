from django.db import models

from testapp.uploaders import DocumentUploader


class Document(models.Model):
    file = models.CharField(max_length=255)

    mount_uploader = DocumentUploader
