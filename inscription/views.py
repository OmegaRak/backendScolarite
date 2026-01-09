# ============================================
# VIEWS INSCRIPTION - CANDIDATS LIBRES
# ============================================
# inscription/views.py

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
import pandas as pd
from django.conf import settings
from django.db import transaction
from django.apps import apps

from .models import (
    Concours, InscriptionConcours, ResultatConcours, 
    Candidat, Etudiant, Formulaire, ResultatBaccalaureat
)
from .serializers import (
    ConcoursSerializer, InscriptionConcoursSerializer, ResultatConcoursSerializer,
    CandidatSerializer, EtudiantSerializer, FormulaireSerializer, ResultatBaccalaureatSerializer
)
from .permissions import IsAdminUser, IsCandidatUser
from auth_users.permissions import IsSuperAdminOrAdmin
from .emails import notifier_admission


# ============================================
# CONCOURS - Candidats voient TOUS les concours
# ============================================

class ConcoursListCreateView(generics.ListCreateAPIView):
    """
    ✅ GET : Liste des concours selon le rôle
         - Public/Candidat : TOUS les concours disponibles
         - Admin : SEULEMENT son établissement
         - SuperAdmin : TOUS
    ✅ POST : Créer un concours (Admin/SuperAdmin)
    """
    serializer_class = ConcoursSerializer
    
    def get_queryset(self):
        """✅ CORRECTION : Filtrage selon le rôle"""
        user = self.request.user
        
        # Si l'utilisateur n'est pas authentifié (public)
        if not user.is_authenticated:
            return Concours.objects.filter(statut='DISPONIBLE').select_related('etablissement')
        
        # SUPERADMIN voit tout
        if user.role == 'SUPERADMIN':
            return Concours.objects.all().select_related('etablissement')
        
        # ✅ ADMIN voit SEULEMENT son établissement
        if user.role == 'ADMIN':
            if not user.etablissement:
                return Concours.objects.none()
            return Concours.objects.filter(
                etablissement=user.etablissement
            ).select_related('etablissement')
        
        # CANDIDAT/ETUDIANT voient tous les concours disponibles
        return Concours.objects.filter(statut='DISPONIBLE').select_related('etablissement')
    
    def get_permissions(self):
        """Permissions selon la méthode"""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'ADMIN':
            if not user.etablissement:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({"error": "Vous n'êtes assigné à aucun établissement"})
            
            serializer.save(etablissement=user.etablissement)

        elif user.role == 'SUPERADMIN':
            if 'etablissement' not in self.request.data:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({"error": "Le SuperAdmin doit spécifier l'établissement"})
            serializer.save()

        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les admins peuvent créer des concours")


class ConcoursRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Concours.objects.all()
    serializer_class = ConcoursSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPERADMIN':
            return Concours.objects.all()
        # Admin voit seulement son établissement
        return Concours.objects.filter(etablissement=user.etablissement)


# ============================================
# INSCRIPTION - Candidats libres, validation par BAC
# ============================================

class InscriptionConcoursCreateView(generics.CreateAPIView):
    """
    ✅ Un candidat s'inscrit à N'IMPORTE QUEL concours
    ✅ SEULE VALIDATION : Admis au BAC (via numero_inscription)
    ✅ AUCUNE restriction par établissement
    """
    serializer_class = InscriptionConcoursSerializer
    permission_classes = [IsAuthenticated, IsCandidatUser]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        utilisateur = request.user
        concours_id = request.data.get('concours')
        justificatif = request.data.get('justificatif_paiement', None)
        numero_inscription = request.data.get('numero_inscription', None)

        if not concours_id:
            return Response({"error": "Le champ 'concours' est obligatoire."}, status=400)
        if not numero_inscription:
            return Response({"error": "Le numéro d'inscription au bac est obligatoire."}, status=400)

        # Vérifier que le concours existe
        try:
            concours = Concours.objects.get(pk=concours_id)
        except Concours.DoesNotExist:
            return Response({"error": "Concours introuvable."}, status=404)
        
        # ✅ AUCUNE VÉRIFICATION d'établissement
        # Le candidat peut s'inscrire à n'importe quel concours

        # ✅ SEULE VALIDATION : Vérifier si admis au BAC
        bac_result = ResultatBaccalaureat.objects.filter(
            numero_inscription=numero_inscription,
            admis=True
        ).first()

        if not bac_result:
            return Response({
                "error": "Inscription impossible : vous devez être admis au baccalauréat.",
                "details": f"Aucun résultat BAC trouvé pour le numéro {numero_inscription} ou vous n'êtes pas admis."
            }, status=400)

        # Création/MAJ inscription
        inscription, created = InscriptionConcours.objects.update_or_create(
            utilisateur=utilisateur,
            concours=concours,
            defaults={
                "justificatif_paiement": justificatif,
                "numero_inscription": numero_inscription
            }
        )

        serializer = self.get_serializer(inscription, context={'request': request})
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class ListeInscriptionsView(generics.ListAPIView):
    """
    ✅ ADMIN : Voit les inscriptions de son établissement UNIQUEMENT
    ✅ CANDIDAT : Voit ses propres inscriptions
    """
    serializer_class = InscriptionConcoursSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # ✅ ADMIN : Filtre par établissement
        if user.role == 'ADMIN':
            return InscriptionConcours.objects.filter(
                concours__etablissement=user.etablissement
            ).select_related('utilisateur', 'concours')
        
        # ✅ SUPERADMIN : Voit tout
        if user.role == 'SUPERADMIN':
            return InscriptionConcours.objects.all().select_related('utilisateur', 'concours')
        
        # ✅ CANDIDAT : Ses propres inscriptions
        return InscriptionConcours.objects.filter(utilisateur=user).select_related('concours')


class InscriptionConcoursUpdateStatusView(generics.RetrieveUpdateAPIView):
    queryset = InscriptionConcours.objects.all()
    serializer_class = InscriptionConcoursSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAdmin]
    http_method_names = ['patch']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPERADMIN':
            return InscriptionConcours.objects.all()
        # Admin voit seulement son établissement
        return InscriptionConcours.objects.filter(concours__etablissement=user.etablissement)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        statut = request.data.get('statut', None)
        if statut not in ['EN_ATTENTE','VALIDÉ','ANNULÉ']:
            return Response({"error":"Statut invalide."}, status=400)
        instance.statut = statut
        instance.save()
        return Response(self.get_serializer(instance, context={'request': request}).data)


# ============================================
# RÉSULTATS (avec filtrage admin)
# ============================================

class ResultatConcoursImportView(APIView):
    """
    ✅ Admin importe les résultats pour son établissement
    ✅ SuperAdmin peut importer pour n'importe quel établissement
    """
    permission_classes = [IsAuthenticated, IsSuperAdminOrAdmin]
    parser_classes = (MultiPartParser, FormParser)

    @transaction.atomic
    def post(self, request):
        if "fichier" not in request.FILES:
            return Response({"error": "Fichier manquant"}, status=400)

        fichier = request.FILES["fichier"]

        try:
            df = pd.read_csv(fichier) if fichier.name.endswith(".csv") else pd.read_excel(fichier)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        Utilisateur = apps.get_model(settings.AUTH_USER_MODEL)
        resultats = []
        erreurs = []

        for index, row in df.iterrows():
            concours_nom = str(row.get("concours")).strip()
            nom = str(row.get("nom")).strip()
            prenom = str(row.get("prenom")).strip()
            email = str(row.get("email", "")).strip()

            try:
                note = float(row.get("note"))
            except:
                erreurs.append(f"Ligne {index+2} : note invalide")
                continue

            # ✅ Filtrer les concours par établissement de l'admin
            concours_qs = Concours.objects.filter(nom__iexact=concours_nom)
            
            if request.user.role == 'ADMIN':
                # Admin ne peut importer que pour son établissement
                concours_qs = concours_qs.filter(etablissement=request.user.etablissement)
            
            concours = concours_qs.first()
            if not concours:
                erreurs.append(f"Ligne {index+2} : concours introuvable ou non autorisé")
                continue

            # Recherche utilisateur
            utilisateur = None
            if email:
                utilisateur = Utilisateur.objects.filter(email__iexact=email).first()
            if not utilisateur:
                utilisateur = Utilisateur.objects.filter(
                    first_name__iexact=prenom,
                    last_name__iexact=nom
                ).first()
            if not utilisateur:
                erreurs.append(f"Ligne {index+2} : utilisateur introuvable")
                continue

            admis = note >= (concours.note_deliberation or 0)

            resultat, _ = ResultatConcours.objects.update_or_create(
                concours=concours,
                utilisateur=utilisateur,
                defaults={
                    "note": note,
                    "admis": admis,
                    "classement": row.get("classement")
                }
            )

            # Passage candidat → étudiant
            if admis and utilisateur.role == 'CANDIDAT':
                utilisateur.role = "ETUDIANT"
                # ✅ Assigner l'établissement du concours à l'étudiant
                utilisateur.etablissement = concours.etablissement
                utilisateur.save(update_fields=["role", "etablissement"])

                candidat = getattr(utilisateur, "candidat_profile", None)
                if not candidat:
                    candidat = Candidat.objects.create(utilisateur=utilisateur)
                
                if not hasattr(candidat, "etudiant_profile"):
                    Etudiant.objects.create(
                        candidat=candidat,
                        matricule=f"{concours.etablissement.code}-{concours.id:03d}-{utilisateur.id:04d}"
                    )

            # Envoi mail
            try:
                notifier_admission(utilisateur, concours, admis)
            except Exception as e:
                erreurs.append(f"Ligne {index+2} : erreur mail - {str(e)}")

            resultats.append(resultat)

        serializer = ResultatConcoursSerializer(resultats, many=True, context={"request": request})

        return Response({
            "status": "success",
            "importes": len(resultats),
            "erreurs": erreurs,
            "resultats": serializer.data
        }, status=201)


class ListeResultatsView(generics.ListAPIView):
    """
    ✅ Admin: résultats de son établissement
    ✅ Étudiant: ses propres résultats
    """
    serializer_class = ResultatConcoursSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'ADMIN':
            return ResultatConcours.objects.filter(
                concours__etablissement=user.etablissement
            ).select_related('utilisateur', 'concours')
        
        if user.role == 'SUPERADMIN':
            return ResultatConcours.objects.all().select_related('utilisateur', 'concours')
        
        return ResultatConcours.objects.filter(utilisateur=user).select_related('concours')


# ============================================
# BAC (pas de filtrage - données globales)
# ============================================

class ResultatBaccalaureatImportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if request.user.role not in ['ADMIN', 'SUPERADMIN']:
            return Response({"error": "Accès refusé"}, status=403)

        if "fichier" not in request.FILES:
            return Response({"error": "Envoyer un fichier Excel/CSV via 'fichier'."}, status=400)

        fichier = request.FILES["fichier"]

        try:
            df = pd.read_csv(fichier) if fichier.name.lower().endswith(".csv") else pd.read_excel(fichier)
        except Exception as e:
            return Response({"error": f"Impossible de lire le fichier : {str(e)}"}, status=400)

        required_columns = ["numero_inscription", "nom", "prenom", "status", "annee_scolaire"]
        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Colonne manquante : {col}"}, status=400)

        resultats_ok = []
        erreurs = []

        for index, row in df.iterrows():
            numero = str(row["numero_inscription"]).strip()
            nom = str(row["nom"]).strip()
            prenom = str(row["prenom"]).strip()
            status_admis = str(row["status"]).strip().upper()
            annee = str(row["annee_scolaire"]).strip()

            admis = status_admis == "ADMIS"

            try:
                resultat, created = ResultatBaccalaureat.objects.update_or_create(
                    numero_inscription=numero,
                    defaults={
                        "nom": nom,
                        "prenom": prenom,
                        "annee_scolaire": annee,
                        "admis": admis
                    }
                )
                resultats_ok.append(resultat)
            except Exception as e:
                erreurs.append(f"Ligne {index + 2} : {str(e)}")

        serializer = ResultatBaccalaureatSerializer(resultats_ok, many=True)

        return Response({
            "status": "success",
            "importes": len(resultats_ok),
            "erreurs": erreurs,
            "resultats": serializer.data
        }, status=201)


class ResultatBaccalaureatListView(generics.ListAPIView):
    serializer_class = ResultatBaccalaureatSerializer
    permission_classes = [IsAuthenticated]
    queryset = ResultatBaccalaureat.objects.all().order_by('-annee_scolaire')


# Autres vues CRUD (inchangées)
class CandidatListCreateView(generics.ListCreateAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAdmin]

class EtudiantListCreateView(generics.ListCreateAPIView):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAdmin]

class FormulaireListCreateView(generics.ListCreateAPIView):
    queryset = Formulaire.objects.all()
    serializer_class = FormulaireSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAdmin]