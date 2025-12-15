from rest_framework import serializers
from .models import Concours, InscriptionConcours, ResultatConcours, Candidat, Etudiant, Formulaire

class ConcoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concours
        fields = '__all__'

class InscriptionConcoursSerializer(serializers.ModelSerializer):
    utilisateur_id = serializers.IntegerField(source='utilisateur.id', read_only=True)
    utilisateur_username = serializers.CharField(source='utilisateur.username', read_only=True)
    utilisateur_nom = serializers.CharField(source='utilisateur.last_name', read_only=True)
    utilisateur_prenom = serializers.CharField(source='utilisateur.first_name', read_only=True)
    utilisateur_email = serializers.CharField(source='utilisateur.email', read_only=True)
    utilisateur_role = serializers.CharField(source='utilisateur.role', read_only=True)

    justificatif_paiement_url = serializers.SerializerMethodField()

    class Meta:
        model = InscriptionConcours
        fields = [
            'id','utilisateur','utilisateur_id','utilisateur_username','utilisateur_nom',
            'utilisateur_prenom','utilisateur_email','utilisateur_role',
            'concours','date_inscription','statut','justificatif_paiement','justificatif_paiement_url',
            'numero_inscription'  # ajouté ici
        ]
        read_only_fields = ('utilisateur', 'date_inscription', 'statut')

    def get_justificatif_paiement_url(self, obj):
        request = self.context.get('request')
        if obj.justificatif_paiement and hasattr(obj.justificatif_paiement, 'url') and request:
            return request.build_absolute_uri(obj.justificatif_paiement.url)
        return None



class ResultatConcoursSerializer(serializers.ModelSerializer):
    utilisateur_id = serializers.IntegerField(source='utilisateur.id', read_only=True)
    utilisateur_first_name = serializers.CharField(source='utilisateur.first_name', read_only=True)
    utilisateur_last_name = serializers.CharField(source='utilisateur.last_name', read_only=True)
    utilisateur_email = serializers.CharField(source='utilisateur.email', read_only=True)
    concours_id = serializers.IntegerField(source='concours.id', read_only=True)
    concours_nom = serializers.CharField(source='concours.nom', read_only=True)

    class Meta:
        model = ResultatConcours
        fields = [
            'id','concours','concours_id','concours_nom',
            'utilisateur','utilisateur_id','utilisateur_first_name','utilisateur_last_name','utilisateur_email',
            'note','classement','admis','date_publication'
        ]


class CandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = '__all__'
        read_only_fields = ('date_candidature',)


class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = '__all__'


class FormulaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulaire
        fields = '__all__'
        read_only_fields = ('date_soumission',)
