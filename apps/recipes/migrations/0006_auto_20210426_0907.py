# Generated by Django 3.2 on 2021-04-26 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20210426_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientline',
            name='recipe',
        ),
        migrations.AddField(
            model_name='ingredientline',
            name='recipe_edition',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_lines', to='recipes.recipeedition'),
            preserve_default=False,
        ),
    ]
