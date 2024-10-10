from django.core.validators import RegexValidator
from django.db import models

class Category(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z ]+$',
                message="Le titre de la catégorie ne doit contenir que des lettres et des espaces."
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
