from rest_framework import serializers
from .models import AnneeScolaire, Reinscription, Niveau, ResultatNiveau

class AnneeScolaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeScolaire
        fields = '__all__'

class ReinscriptionSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.CharField(source='utilisateur.get_full_name', read_only=True)
    annee_libelle = serializers.CharField(source='annee_scolaire.libelle', read_only=True)
    classe = serializers.CharField(source='concours.nom', read_only=True)
    class Meta:
        model = Reinscription
        fields = '__all__'
        read_only_fields = ('utilisateur','statut','date_soumission','date_modification')

class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = '__all__'

class ResultatNiveauSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.CharField(source='utilisateur.get_full_name', read_only=True)
    niveau_nom = serializers.CharField(source='niveau.nom', read_only=True)
    annee_libelle = serializers.CharField(source='annee_scolaire.libelle', read_only=True)

    class Meta:
        model = ResultatNiveau
        fields = ['id','utilisateur','utilisateur_nom','niveau','niveau_nom','annee_scolaire','annee_libelle','moyenne','admis','remarque','created_at']
