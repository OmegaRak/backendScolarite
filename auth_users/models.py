from django.db import models
from django.contrib.auth.models import AbstractUser

# ============================================
# ETABLISSEMENT
# ============================================

class Etablissement(models.Model):
    """Représente un établissement universitaire (ENI, EMIT, etc.)"""
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=100, default="Fianarantsoa")
    adresse = models.TextField(blank=True)
    email_contact = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='etablissements/', null=True, blank=True)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f"{self.code} - {self.nom}"


# ============================================
# UTILISATEUR
# ============================================

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'Super Administrateur'),
        ('ADMIN', 'Administrateur'),
        ('CANDIDAT', 'Candidat'),
        ('ETUDIANT', 'Étudiant'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='CANDIDAT')

    etablissement = models.ForeignKey(
        Etablissement,
        on_delete=models.SET_NULL,  # Sécurisé si établissement supprimé
        null=True,
        blank=True,
        related_name='utilisateurs'
    )

    etudiant = models.OneToOneField(
        'inscription.Etudiant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='utilisateur_auth_etudiant'
    )

    email = models.EmailField(unique=True)

    def is_superadmin(self):
        return self.role == 'SUPERADMIN'

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_candidat(self):
        return self.role == 'CANDIDAT'

    def is_etudiant(self):
        return self.role == 'ETUDIANT'

    def __str__(self):
        etab = f" ({self.etablissement.code})" if self.etablissement else ""
        return f"{self.username}{etab}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['etablissement', 'email'],
                condition=models.Q(role='ADMIN'),
                name='unique_admin_per_etablissement'
            )
        ]
