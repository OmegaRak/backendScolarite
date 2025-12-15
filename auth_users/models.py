from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('CANDIDAT', 'Candidat'),
        ('ETUDIANT', 'Étudiant'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='CANDIDAT')

    # relation vers Etudiant via settings.AUTH_USER_MODEL usage in inscription app
    etudiant = models.OneToOneField(
        'inscription.Etudiant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='utilisateur_auth_etudiant'
    )

    email = models.EmailField(unique=True)

    def is_admin(self):
        return self.role == 'ADMIN'

    def __str__(self):
        return self.username
