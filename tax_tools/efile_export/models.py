from django.db import models


class Efile_Metadata(models.Model):
    parent_sked = models.CharField(max_length=255, null=False)
    parent_sked_part = models.CharField(max_length=255, null=False)
    ordering = models.IntegerField(null=False)

    class Meta:
        abstract = True


class Field_Metadata(Efile_Metadata):
    in_a_group = models.BooleanField(null=False)
    db_table = models.CharField(max_length=255, null=False)
    db_name = models.CharField(max_length=255, null=False)
    xpath = models.CharField(max_length=510, null=False)
    irs_type = models.CharField(max_length=255, null=False)
    db_type = models.CharField(max_length=255, null=False)
    line_number = models.IntegerField(null=False)
    description = models.TextField(null=False)
    versions = models.CharField(max_length=255, null=False)


class Schedule_Part_Metadata(Efile_Metadata):
    part_name = models.CharField(
        "verbose schedule part name",
        max_length=255,
        null=False
    )
    xml_root = models.CharField(max_length=255, null=False)
    is_shell = models.BooleanField(null=False)
