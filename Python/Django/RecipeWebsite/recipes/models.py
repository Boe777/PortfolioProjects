# RecipeWebsite/recipes/models.py

from django.db import models

class Meal(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    instructions = models.TextField()
    ingredients = models.TextField()

    def __str__(self):
        return self.name
