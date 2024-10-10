from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import Conference


class Participant(AbstractUser):
    cin = models.CharField(primary_key=True, max_length=8)
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)
    participant_category = models.CharField(
        max_length=255, 
        choices=(
        ('etudiant', 'étudiant'),
        ('enseignant', 'enseignant'),
        ('doctorant', 'doctorant'),
        ('chercheur', 'chercheur'))
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

class Reservation(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('conference', 'participant')