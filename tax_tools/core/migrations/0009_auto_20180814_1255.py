# Generated by Django 2.0.6 on 2018-08-14 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180814_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiscal_year',
            name='fiscal_year',
            field=models.IntegerField(db_index=True),
        ),
    ]