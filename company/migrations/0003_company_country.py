# Generated by Django 3.1.2 on 2020-11-09 10:29

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20201109_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='country',
            field=django_countries.fields.CountryField(max_length=100, null=True),
        ),
    ]