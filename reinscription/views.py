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

from .models import Reinscription, AnneeScolaire, Niveau, ResultatNiveau
from .serializers import (
    ReinscriptionSerializer,
    AnneeScolaireSerializer,
    ResultatNiveauSerializer,
)

# ==================== Création / Mise à jour d'une réinscription ====================
class ReinscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data.copy()
        required_fields = ['annee_scolaire', 'niveau_actuel', 'niveau_vise', 'concours']
        for field in required_fields:
            if field not in data:
                return Response({"error": f"Le champ {field} est obligatoire"}, status=400)
        
        annee_scolaire_id = data.get('annee_scolaire')
        try:
            existing = Reinscription.objects.filter(utilisateur=request.user, annee_scolaire_id=annee_scolaire_id).first()
            if existing:
                existing.niveau_actuel = data.get('niveau_actuel')
                existing.niveau_vise = data.get('niveau_vise')
                existing.concours_id = data.get('concours')
                if 'dossier_pdf' in request.FILES:
                    existing.dossier_pdf = request.FILES['dossier_pdf']
                if 'bordereau' in request.FILES:
                    existing.bordereau = request.FILES['bordereau']
                if existing.statut == 'REFUSEE':
                    existing.statut = 'EN_ATTENTE'
                existing.save()
                serializer = ReinscriptionSerializer(existing)
                return Response({"message": "Réinscription mise à jour", "data": serializer.data, "updated": True}, status=200)
            else:
                if 'dossier_pdf' not in request.FILES:
                    return Response({"error": "Le dossier PDF est obligatoire"}, status=400)
                serializer = ReinscriptionSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(utilisateur=request.user)
                    return Response({"message": "Réinscription créée", "data": serializer.data, "updated": False}, status=201)
                return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": f"Erreur : {str(e)}"}, status=500)


# ==================== Liste pour admin ====================
class ReinscriptionListAdminView(generics.ListAPIView):
    serializer_class = ReinscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Reinscription.objects.select_related('utilisateur', 'annee_scolaire', 'concours').all()
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

    def get(self, request, *args, **kwargs):
        if getattr(request.user, 'role', None) != 'ADMIN':
            return Response({"error": "Accès refusé"}, status=403)
        return super().get(request, *args, **kwargs)


# ==================== Validation par admin ====================
class ReinscriptionValidationView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if getattr(request.user, 'role', None) != 'ADMIN':
            return Response({"error": "Accès refusé"}, status=403)
        try:
            reins = Reinscription.objects.get(pk=pk)
        except Reinscription.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)
        
        statut = request.data.get('statut')
        if statut not in ['VALIDEE', 'REFUSEE', 'EN_ATTENTE']:
            return Response({"error": "Statut invalide"}, status=400)
        
        reins.statut = statut
        reins.save()
        serializer = ReinscriptionSerializer(reins)
        return Response({"message": "Statut mis à jour", "data": serializer.data})


# ==================== CRUD AnneeScolaire ====================
class AnneeScolaireListCreateView(generics.ListCreateAPIView):
    queryset = AnneeScolaire.objects.all()
    serializer_class = AnneeScolaireSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method == 'GET':
            return AnneeScolaire.objects.filter(actif=True)
        return AnneeScolaire.objects.all()

    def create(self, request, *args, **kwargs):
        if getattr(request.user, 'role', None) != 'ADMIN':
            return Response({"error": "Accès refusé"}, status=403)
        return super().create(request, *args, **kwargs)


# ==================== Liste des niveaux ====================
class NiveauxListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if getattr(request.user, 'role', None) != 'ADMIN':
            return Response({"error": "Accès refusé"}, status=403)
        niveaux = Reinscription.objects.values_list('niveau_vise', flat=True).distinct()
        return Response({"niveaux": sorted(list(niveaux))})


# ==================== Import des résultats ====================
class ResultatNiveauImportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if getattr(request.user, 'role', None) != 'ADMIN':
            return Response({"error":"Accès refusé"}, status=403)
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
            numero, nom, prenom = str(row["numero_inscription"]).strip(), str(row["nom"]).strip(), str(row["prenom"]).strip()
            annee_lib, niveau_nom = str(row["annee"]).strip(), str(row["niveau"]).strip()
            try:
                moyenne = float(row["moyenne"])
            except:
                erreurs.append(f"Ligne {index+2}: moyenne invalide ({row['moyenne']}).")
                continue

            annee = AnneeScolaire.objects.filter(libelle__iexact=annee_lib).first()
            if not annee:
                erreurs.append(f"Ligne {index+2}: année '{annee_lib}' introuvable.")
                continue

            niveau = Niveau.objects.filter(nom__iexact=niveau_nom).first()
            if not niveau:
                erreurs.append(f"Ligne {index+2}: niveau '{niveau_nom}' introuvable.")
                continue

            utilisateur = Utilisateur.objects.filter(first_name__iexact=prenom, last_name__iexact=nom).first()
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
                defaults={"moyenne": moyenne, "admis": admis, "remarque": "ADMIS" if admis else "NON ADMIS"}
            )
            resultats_ok.append(resultat)

        return Response({
            "status": "success",
            "importes": len(resultats_ok),
            "erreurs": erreurs,
            "resultats": ResultatNiveauSerializer(resultats_ok, many=True).data
        }, status=201)


# ==================== NOUVEAU : LISTES FRONTEND ====================
class ReinscriptionListUserView(generics.ListAPIView):
    """Lister les réinscriptions pour l'étudiant connecté"""
    serializer_class = ReinscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reinscription.objects.filter(utilisateur=self.request.user).select_related('annee_scolaire', 'concours').order_by('-date_soumission')


class ResultatNiveauListView(generics.ListAPIView):
    """Lister les résultats pour le frontend"""
    serializer_class = ResultatNiveauSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ResultatNiveau.objects.select_related('utilisateur', 'niveau', 'annee_scolaire').all()

        if getattr(self.request.user, 'role', None) != 'ADMIN':
            queryset = queryset.filter(utilisateur=self.request.user)

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

class ResultatNiveauEtudiantView(generics.ListAPIView):
    serializer_class = ResultatNiveauSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ResultatNiveau.objects.filter(
            utilisateur=self.request.user
        ).select_related('niveau', 'annee_scolaire')

class MesResultatsCompletsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        resultat_concours = ResultatConcours.objects.filter(
            utilisateur=user
        ).first()

        resultats_niveau = ResultatNiveau.objects.filter(
            utilisateur=user
        ).select_related('niveau', 'annee_scolaire') \
         .order_by('annee_scolaire__id')

        return Response({
            "concours": ResultatConcoursSerializer(resultat_concours).data
            if resultat_concours else None,
            "niveaux": ResultatNiveauSerializer(resultats_niveau, many=True).data
        })
