# Generated by Django 3.2 on 2021-07-30 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_host_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='preparation_section',
        ),
    ]