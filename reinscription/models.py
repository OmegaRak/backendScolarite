# ============================================
# MODIFICATIONS DES MODÈLES RÉINSCRIPTION
# ============================================
# reinscription/models.py

from django.db import models
from django.conf import settings

class AnneeScolaire(models.Model):
    """✅ AJOUT : Lien vers établissement"""
    etablissement = models.ForeignKey(
        'auth_users.Etablissement',
        on_delete=models.CASCADE,
        related_name='annees_scolaires'
    )
    
    libelle = models.CharField(max_length=20)  # ex: "2024-2025"
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-libelle']
        # Une année unique par établissement
        unique_together = ('etablissement', 'libelle')

    def __str__(self):
        return f"{self.libelle} ({self.etablissement.code})"


class Niveau(models.Model):
    """✅ AJOUT : Lien vers établissement"""
    etablissement = models.ForeignKey(
        'auth_users.Etablissement',
        on_delete=models.CASCADE,
        related_name='niveaux'
    )
    
    nom = models.CharField(max_length=50)
    seuil_deliberation = models.FloatField(default=10.0)
    ordre = models.IntegerField(default=0)  # Pour trier L1, L2, L3...

    class Meta:
        ordering = ['etablissement', 'ordre']
        # Un niveau unique par établissement
        unique_together = ('etablissement', 'nom')

    def __str__(self):
        return f"{self.nom} ({self.etablissement.code})"


class Reinscription(models.Model):
    """Pas de modification - l'isolation vient de l'année scolaire"""
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reinscriptions')
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, related_name='reinscriptions')
    concours = models.ForeignKey('inscription.Concours', on_delete=models.SET_NULL, null=True, blank=True)
    niveau_actuel = models.CharField(max_length=100)
    niveau_vise = models.CharField(max_length=100)
    dossier_pdf = models.FileField(upload_to='reinscriptions/')
    bordereau = models.FileField(upload_to='versements/', null=True, blank=True)
    statut_choices = (('EN_ATTENTE','En attente'),('VALIDEE','Validée'),('REFUSEE','Refusée'))
    statut = models.CharField(max_length=20, choices=statut_choices, default='EN_ATTENTE')
    date_soumission = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('utilisateur', 'annee_scolaire')
        ordering = ['-date_soumission']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.annee_scolaire.libelle}"


class ResultatNiveau(models.Model):
    """Pas de modification - l'isolation vient du niveau"""
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resultats_niveau')
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='resultats')
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, related_name='resultats_niveau')
    moyenne = models.FloatField()
    admis = models.BooleanField(default=False)
    remarque = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'niveau', 'annee_scolaire')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.niveau.nom} - {self.annee_scolaire.libelle}"