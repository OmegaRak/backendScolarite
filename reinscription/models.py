from django.db import models
from django.conf import settings

class AnneeScolaire(models.Model):
    libelle = models.CharField(max_length=20)  # ex: "2024-2025"
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.libelle

class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    seuil_deliberation = models.FloatField(default=10.0)

    def __str__(self):
        return self.nom

class Reinscription(models.Model):
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
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resultats_niveau')
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='resultats')
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, related_name='resultats_niveau')
    moyenne = models.FloatField()
    admis = models.BooleanField(default=False)
    remarque = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'niveau', 'annee_scolaire')
