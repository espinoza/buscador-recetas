# Generated by Django 3.2 on 2021-04-24 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210419_0703'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
    ]
