# ============================================
# SERIALIZERS AUTH - COMPLET
# ============================================
# auth_users/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

# ============================================
# SERIALIZER REGISTRATION
# ============================================

class UtilisateurRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouvel utilisateur.
    ✅ Accepte first_name et last_name (format Django standard)
    """
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        label='Confirmer le mot de passe'
    )

    class Meta:
        model = Utilisateur
        fields = [
            'username', 
            'email', 
            'first_name',  # ✅ Django standard
            'last_name',   # ✅ Django standard
            'password', 
            'password2', 
            'role'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate_email(self, value):
        """Vérifier que l'email est unique"""
        if Utilisateur.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un utilisateur avec cet email existe déjà.")
        return value

    def validate_username(self, value):
        """Vérifier que le username est unique"""
        if Utilisateur.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return value

    def validate(self, attrs):
        """Validation globale"""
        # Vérifier que les mots de passe correspondent
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password2": "Les mots de passe ne correspondent pas."
            })
        
        # Vérifier le rôle
        role = attrs.get('role', 'CANDIDAT')
        
        # Empêcher la création de SUPERADMIN et ADMIN via l'API publique
        if role in ['SUPERADMIN', 'ADMIN']:
            raise serializers.ValidationError({
                "role": "Vous ne pouvez pas créer un compte avec ce rôle."
            })
        
        return attrs

    def create(self, validated_data):
        """Créer l'utilisateur"""
        # Retirer password2 (pas dans le modèle)
        validated_data.pop('password2')
        
        # Extraire le password
        password = validated_data.pop('password')
        
        # Par défaut CANDIDAT, établissement NULL
        if 'role' not in validated_data:
            validated_data['role'] = 'CANDIDAT'
        
        # L'établissement reste NULL pour les candidats
        validated_data['etablissement'] = None
        
        # Créer l'utilisateur
        user = Utilisateur(**validated_data)
        user.set_password(password)  # Hash le password
        user.save()
        
        return user


# ============================================
# SERIALIZER UTILISATEUR (Profile)
# ============================================

class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour afficher les infos d'un utilisateur.
    Inclut les détails de l'établissement si présent.
    """
    etablissement_details = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'role', 
            'is_active',
            'etablissement',
            'etablissement_details'
        ]
        read_only_fields = ['is_active', 'role']

    def get_etablissement_details(self, obj):
        """Retourner les détails de l'établissement si présent"""
        if obj.etablissement:
            return {
                'id': obj.etablissement.id,
                'code': obj.etablissement.code,
                'nom': obj.etablissement.nom,
                'ville': obj.etablissement.ville
            }
        return None


# ============================================
# SERIALIZER ÉTABLISSEMENT
# ============================================

class EtablissementSerializer(serializers.ModelSerializer):
    """Serializer pour les établissements"""
    nombre_utilisateurs = serializers.SerializerMethodField()
    nombre_admins = serializers.SerializerMethodField()
    nombre_concours = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()._meta.get_field('etablissement').related_model
        fields = [
            'id', 
            'code', 
            'nom', 
            'ville', 
            'adresse', 
            'email_contact', 
            'telephone', 
            'logo', 
            'actif',
            'date_creation',
            'nombre_utilisateurs',
            'nombre_admins',
            'nombre_concours'
        ]
    
    def get_nombre_utilisateurs(self, obj):
        return obj.utilisateurs.count()
    
    def get_nombre_admins(self, obj):
        return obj.utilisateurs.filter(role='ADMIN').count()
    
    def get_nombre_concours(self, obj):
        return obj.concours.count() if hasattr(obj, 'concours') else 0


# ============================================
# SERIALIZER ASSIGNATION ADMIN
# ============================================

class AdminAssignmentSerializer(serializers.Serializer):
    """
    Serializer pour assigner un admin à un établissement.
    Utilisé par le SuperAdmin uniquement.
    """
    utilisateur_id = serializers.IntegerField(required=True)
    etablissement_id = serializers.IntegerField(required=True)

    def validate_utilisateur_id(self, value):
        if not Utilisateur.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Utilisateur introuvable.")
        return value

    def validate_etablissement_id(self, value):
        Etablissement = get_user_model()._meta.get_field('etablissement').related_model
        if not Etablissement.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Établissement introuvable.")
        return value