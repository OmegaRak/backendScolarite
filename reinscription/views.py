from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
import pandas as pd
from django.conf import settings

from inscription.models import ResultatConcours
from inscription.serializers import ResultatConcoursSerializer
from auth_users.permissions import IsSuperAdminOrAdmin, EtablissementFilterMixin

from .models import Reinscription, AnneeScolaire, Niveau, ResultatNiveau
from .serializers import (
    ReinscriptionSerializer,
    AnneeScolaireSerializer,
    ResultatNiveauSerializer,
)


# ==================== ANNÉE SCOLAIRE ====================
class AnneeScolaireListCreateView(generics.ListCreateAPIView):
    """
    GET :
      - SuperAdmin : toutes les années
      - Admin : années actives de son établissement

    POST :
      - SuperAdmin : doit fournir etablissement (optionnel si géré ailleurs)
      - Admin : établissement auto
    """
    serializer_class = AnneeScolaireSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'SUPERADMIN':
            return AnneeScolaire.objects.all()

        if user.role == 'ADMIN' and user.etablissement:
            qs = AnneeScolaire.objects.filter(etablissement=user.etablissement)
            if self.request.method == 'GET':
                return qs.filter(actif=True)
            return qs

        if user.role == 'ETUDIANT':
            # Étudiant peut voir toutes les années actives
            return AnneeScolaire.objects.filter(actif=True)

        return AnneeScolaire.objects.none()


    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'ADMIN':
            # ✅ Auto depuis l'utilisateur connecté
            serializer.save(etablissement=user.etablissement)

        elif user.role == 'SUPERADMIN':
            # ⚠️ Option 1 : superadmin choisit l’établissement
            if not serializer.validated_data.get('etablissement'):
                raise serializers.ValidationError({
                    "etablissement": "Ce champ est obligatoire pour le SuperAdmin"
                })
            serializer.save()

        else:
            raise PermissionError("Seuls les admins peuvent créer une année scolaire")

# ==================== NIVEAUX ====================
class NiveauxListView(APIView):
    """Liste les niveaux visés distincts de l'établissement"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        if user.role not in ['ADMIN', 'SUPERADMIN']:
            return Response({"error": "Accès refusé"}, status=403)
        
        # Filtrer par établissement
        if user.role == 'SUPERADMIN':
            niveaux = Niveau.objects.all()
        else:
            niveaux = Niveau.objects.filter(etablissement=user.etablissement)
        
        # Récupérer les noms distincts
        niveaux_list = niveaux.values_list('nom', flat=True).distinct().order_by('nom')
        
        return Response({"niveaux": list(niveaux_list)})


class NiveauListCreateView(generics.ListCreateAPIView):
    """CRUD complet pour les niveaux"""
    serializer_class = serializers.ModelSerializer
    permission_classes = [IsAuthenticated]
    
    class Meta:
        model = Niveau
        fields = '__all__'

    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'SUPERADMIN':
            return Niveau.objects.all()
        
        if user.etablissement:
            return Niveau.objects.filter(etablissement=user.etablissement)
        
        return Niveau.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role == 'SUPERADMIN':
            serializer.save()
        elif user.role == 'ADMIN':
            serializer.save(etablissement=user.etablissement)
        else:
            raise PermissionError("Accès refusé")


# ==================== RÉINSCRIPTION ====================
class ReinscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data.copy()
        user = request.user

        print("📦 Données reçues:", data)

        required_fields = ['annee_scolaire', 'niveau_actuel', 'niveau_vise', 'concours']
        for field in required_fields:
            if field not in data or data.get(field) in [None, "", "0"]:
                return Response(
                    {"error": f"Le champ {field} est obligatoire"},
                    status=400
                )

        # 🔹 Vérifier existence uniquement (PAS établissement)
        try:
            annee = AnneeScolaire.objects.get(pk=data.get('annee_scolaire'))
        except AnneeScolaire.DoesNotExist:
            return Response({"error": "Année scolaire introuvable"}, status=404)

        try:
            from inscription.models import Concours
            concours = Concours.objects.get(pk=data.get('concours'))
        except Concours.DoesNotExist:
            return Response({"error": "Concours introuvable"}, status=404)

        # 🔹 Vérifier s'il existe déjà une réinscription
        existing = Reinscription.objects.filter(
            utilisateur=user,
            annee_scolaire=annee
        ).first()

        if existing:
            # 🔁 Mise à jour
            existing.niveau_actuel = data.get('niveau_actuel')
            existing.niveau_vise = data.get('niveau_vise')
            existing.concours = concours

            if 'dossier_pdf' in request.FILES:
                existing.dossier_pdf = request.FILES['dossier_pdf']
            if 'bordereau' in request.FILES:
                existing.bordereau = request.FILES['bordereau']

            if existing.statut == 'REFUSEE':
                existing.statut = 'EN_ATTENTE'

            existing.save()

            serializer = ReinscriptionSerializer(existing)
            return Response({
                "message": "Réinscription mise à jour",
                "data": serializer.data,
                "updated": True
            }, status=200)

        # 🆕 Création
        if 'dossier_pdf' not in request.FILES:
            return Response(
                {"error": "Le dossier PDF est obligatoire"},
                status=400
            )

        serializer = ReinscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                utilisateur=user,
                annee_scolaire=annee,
                concours=concours
            )
            return Response({
                "message": "Réinscription créée",
                "data": serializer.data,
                "updated": False
            }, status=201)

        return Response(serializer.errors, status=400)


class ReinscriptionListAdminView(EtablissementFilterMixin, generics.ListAPIView):
    """Liste des réinscriptions (Admin: son établissement, SuperAdmin: tout)"""
    serializer_class = ReinscriptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Reinscription.objects.select_related('utilisateur', 'annee_scolaire', 'concours').all()

    def get(self, request, *args, **kwargs):
        if request.user.role not in ['ADMIN', 'SUPERADMIN']:
            return Response({"error": "Accès refusé"}, status=403)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtres supplémentaires
        niveau_vise = self.request.query_params.get('niveau_vise')
        annee_scolaire = self.request.query_params.get('annee_scolaire')
        statut = self.request.query_params.get('statut')
        concours = self.request.query_params.get('concours')
        search = self.request.query_params.get('search')

        if niveau_vise:
            queryset = queryset.filter(niveau_vise__icontains=niveau_vise)
        if annee_scolaire:
            queryset = queryset.filter(annee_scolaire_id=annee_scolaire)
        if statut:
            queryset = queryset.filter(statut=statut)
        if concours:
            queryset = queryset.filter(concours_id=concours)
        if search:
            queryset = queryset.filter(
                Q(utilisateur__first_name__icontains=search) |
                Q(utilisateur__last_name__icontains=search) |
                Q(utilisateur__email__icontains=search)
            )
        
        return queryset


class ReinscriptionValidationView(APIView):
    """Validation d'une réinscription (Admin)"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = request.user
        
        if user.role not in ['ADMIN', 'SUPERADMIN']:
            return Response({"error": "Accès refusé"}, status=403)
        
        try:
            reins = Reinscription.objects.select_related('annee_scolaire').get(pk=pk)
        except Reinscription.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)
        
        # ✅ Vérifier que la réinscription appartient à l'établissement de l'admin
        if user.role == 'ADMIN':
            if reins.annee_scolaire.etablissement != user.etablissement:
                return Response({"error": "Accès refusé à cette réinscription"}, status=403)
        
        statut = request.data.get('statut')
        if statut not in ['VALIDEE', 'REFUSEE', 'EN_ATTENTE']:
            return Response({"error": "Statut invalide"}, status=400)
        
        reins.statut = statut
        reins.save()
        serializer = ReinscriptionSerializer(reins)
        return Response({"message": "Statut mis à jour", "data": serializer.data})


# ==================== RÉSULTATS NIVEAU ====================
class ResultatNiveauImportView(APIView):
    """Import des résultats de niveau (Admin)"""
    permission_classes = [IsAuthenticated, IsSuperAdminOrAdmin]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if "fichier" not in request.FILES:
            return Response({"error":"Envoyer un fichier Excel/CSV via 'fichier'."}, status=400)
        
        fichier = request.FILES["fichier"]

        try:
            df = pd.read_csv(fichier) if fichier.name.lower().endswith(".csv") else pd.read_excel(fichier)
        except Exception as e:
            return Response({"error": f"Impossible de lire le fichier : {str(e)}"}, status=400)

        required_columns = ["numero_inscription","nom","prenom","annee","niveau","moyenne"]
        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Colonne manquante : {col}"}, status=400)

        from django.apps import apps
        Utilisateur = apps.get_model(settings.AUTH_USER_MODEL)
        resultats_ok = []
        erreurs = []

        for index, row in df.iterrows():
            numero = str(row["numero_inscription"]).strip()
            nom = str(row["nom"]).strip()
            prenom = str(row["prenom"]).strip()
            annee_lib = str(row["annee"]).strip()
            niveau_nom = str(row["niveau"]).strip()
            
            try:
                moyenne = float(row["moyenne"])
            except:
                erreurs.append(f"Ligne {index+2}: moyenne invalide ({row['moyenne']}).")
                continue

            # ✅ Filtrer par établissement de l'admin
            annee_qs = AnneeScolaire.objects.filter(libelle__iexact=annee_lib)
            if request.user.role == 'ADMIN':
                annee_qs = annee_qs.filter(etablissement=request.user.etablissement)
            annee = annee_qs.first()
            
            if not annee:
                erreurs.append(f"Ligne {index+2}: année '{annee_lib}' introuvable ou non autorisée.")
                continue

            # ✅ Filtrer niveau par établissement
            niveau_qs = Niveau.objects.filter(nom__iexact=niveau_nom)
            if request.user.role == 'ADMIN':
                niveau_qs = niveau_qs.filter(etablissement=request.user.etablissement)
            niveau = niveau_qs.first()
            
            if not niveau:
                erreurs.append(f"Ligne {index+2}: niveau '{niveau_nom}' introuvable ou non autorisé.")
                continue

            # Recherche utilisateur
            utilisateur = Utilisateur.objects.filter(
                first_name__iexact=prenom, 
                last_name__iexact=nom
            ).first()
            
            if not utilisateur:
                utilisateur = Utilisateur.objects.filter(username__iexact=numero).first()
            
            if not utilisateur:
                erreurs.append(f"Ligne {index+2}: utilisateur {prenom} {nom} introuvable.")
                continue

            admis = moyenne >= niveau.seuil_deliberation
            resultat, created = ResultatNiveau.objects.update_or_create(
                utilisateur=utilisateur,
                niveau=niveau,
                annee_scolaire=annee,
                defaults={
                    "moyenne": moyenne, 
                    "admis": admis, 
                    "remarque": "ADMIS" if admis else "NON ADMIS"
                }
            )
            resultats_ok.append(resultat)

        return Response({
            "status": "success",
            "importes": len(resultats_ok),
            "erreurs": erreurs,
            "resultats": ResultatNiveauSerializer(resultats_ok, many=True).data
        }, status=201)


class ResultatNiveauListView(EtablissementFilterMixin, generics.ListAPIView):
    """Liste des résultats de niveau (filtré par établissement)"""
    serializer_class = ResultatNiveauSerializer
    permission_classes = [IsAuthenticated]
    queryset = ResultatNiveau.objects.select_related('utilisateur', 'niveau', 'annee_scolaire').all()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtres supplémentaires
        annee = self.request.query_params.get('annee')
        niveau = self.request.query_params.get('niveau')
        utilisateur_id = self.request.query_params.get('utilisateur')

        if annee:
            queryset = queryset.filter(annee_scolaire_id=annee)
        if niveau:
            queryset = queryset.filter(niveau_id=niveau)
        if utilisateur_id:
            queryset = queryset.filter(utilisateur_id=utilisateur_id)

        return queryset


class ReinscriptionListUserView(generics.ListAPIView):
    """Liste des réinscriptions de l'étudiant connecté"""
    serializer_class = ReinscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reinscription.objects.filter(
            utilisateur=self.request.user
        ).select_related('annee_scolaire', 'concours').order_by('-date_soumission')


class ResultatNiveauEtudiantView(generics.ListAPIView):
    """Résultats de niveau de l'étudiant connecté"""
    serializer_class = ResultatNiveauSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ResultatNiveau.objects.filter(
            utilisateur=self.request.user
        ).select_related('niveau', 'annee_scolaire')


class MesResultatsCompletsView(APIView):
    """Tous les résultats de l'étudiant (concours + niveaux)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        resultat_concours = ResultatConcours.objects.filter(utilisateur=user).first()
        resultats_niveau = ResultatNiveau.objects.filter(
            utilisateur=user
        ).select_related('niveau', 'annee_scolaire').order_by('annee_scolaire__id')

        return Response({
            "concours": ResultatConcoursSerializer(resultat_concours).data if resultat_concours else None,
            "niveaux": ResultatNiveauSerializer(resultats_niveau, many=True).data
        })