# Generated by Django 2.0.6 on 2018-07-19 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_schedule_metadata_parent_form_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule_metadata',
            name='parent_form_type',
        ),
        migrations.AddField(
            model_name='schedule_metadata',
            name='associated_skeds',
            field=models.ManyToManyField(to='core.Schedule_Metadata'),
        ),
    ]
