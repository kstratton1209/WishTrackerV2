from django.db import models
from apps.login.models import Registration
import re

# Create your models here.

class WishesManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['wish']) < 4:
            errors["wish"] = "A wish must consist of at least 3 characters."
        if len(postData['description']) < 1:
            errors["description"] = "A description must be provided!"       
        return errors


class Wishes(models.Model):
    user = models.ForeignKey(Registration, related_name = "user_wishes", on_delete = models.CASCADE)
    wish = models.TextField()
    description = models.TextField()
    granted = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishesManager()

