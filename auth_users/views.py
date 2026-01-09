# ============================================
# VIEWS AUTH - REGISTRATION LIBRE
# ============================================
# auth_users/views.py

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction

from .serializers import (
    UtilisateurRegistrationSerializer, 
    UtilisateurSerializer,
    EtablissementSerializer,
    AdminAssignmentSerializer
)
from .models import Utilisateur, Etablissement
from .permissions import IsSuperAdmin, IsSuperAdminOrAdmin


# ============================================
# GESTION ÉTABLISSEMENTS (SuperAdmin only)
# ============================================

class EtablissementListCreateView(generics.ListCreateAPIView):
    """Liste et création d'établissements (SuperAdmin uniquement)"""
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsSuperAdmin()]
        return [AllowAny()]  # Tout le monde peut voir la liste


class EtablissementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détails/Modification d'un établissement (SuperAdmin uniquement)"""
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer
    permission_classes = [IsSuperAdmin]


# ============================================
# ASSIGNATION ADMIN PAR SUPERADMIN
# ============================================

class AssignAdminToEtablissementView(APIView):
    """
    Le SuperAdmin assigne un utilisateur comme Admin d'un établissement.
    POST: {
        "utilisateur_id": 5,
        "etablissement_id": 2
    }
    """
    permission_classes = [IsSuperAdmin]

    @transaction.atomic
    def post(self, request):
        serializer = AdminAssignmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        utilisateur_id = serializer.validated_data['utilisateur_id']
        etablissement_id = serializer.validated_data['etablissement_id']
        
        try:
            utilisateur = Utilisateur.objects.get(pk=utilisateur_id)
            etablissement = Etablissement.objects.get(pk=etablissement_id)
        except (Utilisateur.DoesNotExist, Etablissement.DoesNotExist):
            return Response({"error": "Utilisateur ou établissement introuvable"}, status=404)
        
        # Vérifier qu'il n'est pas déjà admin ailleurs
        if utilisateur.role == 'ADMIN' and utilisateur.etablissement and utilisateur.etablissement != etablissement:
            return Response({
                "error": f"Cet utilisateur est déjà admin de {utilisateur.etablissement.nom}"
            }, status=400)
        
        # Assignation
        utilisateur.role = 'ADMIN'
        utilisateur.etablissement = etablissement
        utilisateur.save()
        
        return Response({
            "message": f"{utilisateur.username} est maintenant Admin de {etablissement.nom}",
            "utilisateur": UtilisateurSerializer(utilisateur).data
        }, status=200)


class RevokeAdminView(APIView):
    """
    Le SuperAdmin révoque le rôle Admin d'un utilisateur.
    POST: {"utilisateur_id": 5}
    """
    permission_classes = [IsSuperAdmin]

    def post(self, request):
        utilisateur_id = request.data.get('utilisateur_id')
        if not utilisateur_id:
            return Response({"error": "utilisateur_id requis"}, status=400)
        
        try:
            utilisateur = Utilisateur.objects.get(pk=utilisateur_id)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=404)
        
        if utilisateur.role != 'ADMIN':
            return Response({"error": "Cet utilisateur n'est pas Admin"}, status=400)
        
        # Révoquer
        utilisateur.role = 'CANDIDAT'
        utilisateur.etablissement = None
        utilisateur.save()
        
        return Response({
            "message": f"Rôle Admin révoqué pour {utilisateur.username}",
            "utilisateur": UtilisateurSerializer(utilisateur).data
        }, status=200)


# ============================================
# LISTE DES ADMINS (SuperAdmin)
# ============================================

class ListeAdminsView(generics.ListAPIView):
    """Liste tous les admins avec leur établissement"""
    serializer_class = UtilisateurSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        return Utilisateur.objects.filter(role='ADMIN').select_related('etablissement')


# ============================================
# REGISTRATION (AUCUN CHANGEMENT - Libre)
# ============================================
class UtilisateurRegistrationView(generics.CreateAPIView):
    """
    Inscription libre : aucun établissement requis.
    Les candidats resteront CANDIDAT jusqu'à validation via concours.
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurRegistrationSerializer
    permission_classes = [AllowAny]
# ============================================
# JWT TOKEN (Modifié pour inclure établissement)
# ============================================

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        token['etablissement_id'] = user.etablissement.id if user.etablissement else None
        token['etablissement_code'] = user.etablissement.code if user.etablissement else None
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ============================================
# PROFILE
# ============================================

class UtilisateurProfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UtilisateurSerializer(request.user)
        return Response(serializer.data)