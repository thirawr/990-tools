from django.db import models
from core.models import Schedule_Metadata, Schedule_Part_Metadata, Field_Metadata, Organization


class Report(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    author = models.EmailField()
    fields = models.ManyToManyField(Field_Metadata)
    orgs = models.ManyToManyField(Organization)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    marked_for_deletion = models.BooleanField(default=False)
