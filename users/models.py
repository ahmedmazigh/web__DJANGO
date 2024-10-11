from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from conferences.models import Conference


class Participant(AbstractUser):
    cin = models.CharField(
        primary_key=True, 
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le CIN doit contenir exactement 8 chiffres."
            )
        ]
    )
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)
    participant_category = models.CharField(
        max_length=255,
        choices=(
            ('etudiant', 'étudiant'),
            ('enseignant', 'enseignant'),
            ('doctorant', 'doctorant'),
            ('chercheur', 'chercheur')
        )
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name_plural = "Participants"

    def clean(self):
        # Validation de l'email
        if not self.email.endswith('@esprit.tn'):
            raise ValidationError("L'adresse e-mail doit appartenir au domaine esprit.tn.")

class Reservation(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('conference', 'participant')
        verbose_name_plural = "Reservations"

    def clean(self):
        # date future
        if self.conference.start_date <= timezone.now().date():
            raise ValidationError("Vous ne pouvez réserver que des conférences futures.")
        
        # maximum 3 conferences par jour
        reservations_today = Reservation.objects.filter(
            participant=self.participant,
            reservation_date__date=timezone.now().date()
        ).count()

        if reservations_today >= 3:
            raise ValidationError("Vous avez atteint la limite de 3 réservations par jour.")
