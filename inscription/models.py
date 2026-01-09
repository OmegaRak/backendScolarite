# ============================================
# MODIFICATIONS DES MODÈLES INSCRIPTION
# ============================================
# inscription/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class ResultatBaccalaureat(models.Model):
    """Les résultats du bac restent globaux (pas liés à un établissement)"""
    numero_inscription = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    annee_scolaire = models.CharField(max_length=20)
    admis = models.BooleanField(default=False)
    date_import = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.numero_inscription} - {self.nom} {self.prenom}"


class Concours(models.Model):
    """✅ AJOUT : Lien vers établissement"""
    etablissement = models.ForeignKey(
        'auth_users.Etablissement',  # Ajuster selon votre structure
        on_delete=models.CASCADE,
        related_name='concours'
    )
    
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    prix = models.FloatField(default=0)
    note_deliberation = models.FloatField(default=12.0)
    statut_choices = (('DISPONIBLE','Disponible'),('INDISPONIBLE','Indisponible'))
    statut = models.CharField(max_length=20, choices=statut_choices, default='DISPONIBLE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # Un concours unique par établissement et année
        unique_together = ('etablissement', 'nom', 'date_debut')

    def save(self, *args, **kwargs):
        if self.date_fin < timezone.now().date():
            self.statut = 'INDISPONIBLE'
        else:
            self.statut = 'DISPONIBLE'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.etablissement.code})"


class InscriptionConcours(models.Model):
    """Pas de modification nécessaire - l'isolation vient du concours"""
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscriptions')
    concours = models.ForeignKey(Concours, on_delete=models.CASCADE, related_name='inscriptions')
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, default='EN_ATTENTE')
    justificatif_paiement = models.FileField(upload_to='versements/', null=True, blank=True)
    numero_inscription = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('utilisateur', 'concours')
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.utilisateur} - {self.concours}"


class ResultatConcours(models.Model):
    """Pas de modification - l'isolation vient du concours"""
    concours = models.ForeignKey(Concours, on_delete=models.CASCADE, related_name='resultats')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resultats')
    note = models.FloatField()
    classement = models.IntegerField(null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    admis = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_publication']
        unique_together = ('concours', 'utilisateur')

    def __str__(self):
        return f"{self.concours} - {self.utilisateur} : {self.note}"


class Candidat(models.Model):
    """Pas de modification nécessaire"""
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidat_profile')
    statut_candidature = models.CharField(max_length=50, default='EN_ATTENTE')
    date_candidature = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} ({self.utilisateur.etablissement.code if self.utilisateur.etablissement else 'N/A'})"


class Etudiant(models.Model):
    """Pas de modification nécessaire"""
    candidat = models.OneToOneField(Candidat, on_delete=models.CASCADE, related_name='etudiant_profile')
    matricule = models.CharField(max_length=50, unique=True)
    statut_reinscription = models.CharField(max_length=50, default='NON')

    def __str__(self):
        return self.matricule


class Formulaire(models.Model):
    """Pas de modification nécessaire"""
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='formulaires')
    niveau_requis = models.CharField(max_length=255)
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Formulaire {self.pk} - {self.candidat.utilisateur.username}"