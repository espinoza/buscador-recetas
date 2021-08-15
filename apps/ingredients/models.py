from django.db import models


class Ingredient(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IngredientName(models.Model):
    singular = models.CharField(max_length=255)
    plural = models.CharField(max_length=255,
                              blank=True,
                              null=True)
    ingredient = models.ForeignKey(to=Ingredient,
                                   related_name="names",
                                   on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UnknownIngredientName(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
