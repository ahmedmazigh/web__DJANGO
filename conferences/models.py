from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from categories.models import Category


CONF_MAX_CAPACITY = 100

class Conference(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.FloatField()
    capacity = models.IntegerField(
        validators=[MaxValueValidator(CONF_MAX_CAPACITY)]
    )
    program = models.FileField(
        upload_to='files/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def clean(self):
        if self.start_date <= timezone.now().date():
            raise ValidationError("La date de début de la conférence doit être dans le futur.")
        
        if self.end_date <= self.start_date:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")

    class Meta:
        verbose_name_plural = "Conferences"
