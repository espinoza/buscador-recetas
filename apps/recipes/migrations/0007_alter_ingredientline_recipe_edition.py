# Generated by Django 3.2 on 2021-04-26 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20210426_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientline',
            name='recipe_edition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_lines', to='recipes.recipeedition'),
        ),
    ]
