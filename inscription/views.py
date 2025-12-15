from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
import pandas as pd
from django.conf import settings
from django.db import transaction

from .models import Concours, InscriptionConcours, ResultatConcours, Candidat, Etudiant, Formulaire
from .serializers import (
    ConcoursSerializer, InscriptionConcoursSerializer, ResultatConcoursSerializer,
    CandidatSerializer, EtudiantSerializer, FormulaireSerializer
)
from .permissions import IsAdminUser, IsCandidatUser

# -------- Concours --------
class ConcoursListCreateView(generics.ListCreateAPIView):
    queryset = Concours.objects.all()
    serializer_class = ConcoursSerializer
    permission_classes = [AllowAny]

class ConcoursRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Concours.objects.all()
    serializer_class = ConcoursSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# -------- Inscription --------
class InscriptionConcoursCreateView(generics.CreateAPIView):
    """
    Crée une inscription au concours.
    Le champ 'numero_inscription' est envoyé depuis le frontend.
    """
    serializer_class = InscriptionConcoursSerializer
    permission_classes = [IsAuthenticated, IsCandidatUser]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        utilisateur = request.user
        concours_id = request.data.get('concours')
        justificatif = request.data.get('justificatif_paiement', None)
        numero_inscription = request.data.get('numero_inscription', None)  # récupéré depuis frontend

        if not concours_id:
            return Response({"error": "Le champ 'concours' est obligatoire."}, status=400)

        try:
            concours = Concours.objects.get(pk=concours_id)
        except Concours.DoesNotExist:
            return Response({"error": "Concours introuvable."}, status=404)

        # update_or_create pour éviter les doublons
        inscription, created = InscriptionConcours.objects.update_or_create(
            utilisateur=utilisateur,
            concours=concours,
            defaults={
                "justificatif_paiement": justificatif,
                "numero_inscription": numero_inscription  # sauvegarde le numéro
            }
        )

        serializer = self.get_serializer(inscription, context={'request': request})
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class ListeInscriptionsView(generics.ListAPIView):
    serializer_class = InscriptionConcoursSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'ADMIN':
            return InscriptionConcours.objects.all()
        return InscriptionConcours.objects.filter(utilisateur=user)


class InscriptionConcoursUpdateStatusView(generics.RetrieveUpdateAPIView):
    queryset = InscriptionConcours.objects.all()
    serializer_class = InscriptionConcoursSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        statut = request.data.get('statut', None)
        if statut not in ['EN_ATTENTE','VALIDÉ','ANNULÉ']:
            return Response({"error":"Statut invalide."}, status=400)
        instance.statut = statut
        instance.save()
        return Response(self.get_serializer(instance, context={'request': request}).data)

# -------- Résultats --------
class ResultatConcoursImportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    @transaction.atomic
    def post(self, request):
        if "fichier" not in request.FILES:
            return Response({"error":"Envoyer un fichier Excel/CSV via 'fichier'."}, status=400)
        fichier = request.FILES["fichier"]
        try:
            if fichier.name.lower().endswith(".csv"):
                df = pd.read_csv(fichier)
            else:
                df = pd.read_excel(fichier)
        except Exception as e:
            return Response({"error": f"Impossible de lire le fichier : {str(e)}"}, status=400)

        required_columns = ["concours","nom","prenom","note"]
        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Colonne manquante : {col}"}, status=400)

        resultats_importes = []
        erreurs = []

        from django.apps import apps
        Utilisateur = apps.get_model(settings.AUTH_USER_MODEL)

        for index, row in df.iterrows():
            concours_nom = str(row["concours"]).strip()
            nom = str(row["nom"]).strip()
            prenom = str(row["prenom"]).strip()
            try:
                note = float(row["note"])
            except Exception:
                erreurs.append(f"Ligne {index+2}: note invalide ({row['note']}).")
                continue

            concours = Concours.objects.filter(nom__iexact=concours_nom).first()
            if not concours:
                erreurs.append(f"Ligne {index+2}: Concours '{concours_nom}' introuvable.")
                continue

            utilisateur = Utilisateur.objects.filter(first_name__iexact=prenom, last_name__iexact=nom).first()
            if not utilisateur:
                utilisateur = Utilisateur.objects.filter(username__iexact=f"{prenom}.{nom}").first()
            if not utilisateur:
                erreurs.append(f"Ligne {index+2}: Candidat '{nom} {prenom}' introuvable.")
                continue

            admis_bool = note >= (concours.note_deliberation or 0)

            resultat, created = ResultatConcours.objects.update_or_create(
                concours=concours,
                utilisateur=utilisateur,
                defaults={
                    "note": note,
                    "classement": row.get("classement", None),
                    "admis": admis_bool
                }
            )

            # Mise à jour role et Etudiant
            if admis_bool and getattr(utilisateur, 'role', None) != 'ADMIN':
                utilisateur.role = 'ETUDIANT'
                utilisateur.save(update_fields=['role'])

                candidat = getattr(utilisateur, 'candidat_profile', None)
                if candidat and not hasattr(candidat, 'etudiant_profile'):
                    matricule = f"{concours.id:03d}-{utilisateur.id:04d}"
                    Etudiant.objects.create(candidat=candidat, matricule=matricule)

            resultats_importes.append(resultat)

        serializer = ResultatConcoursSerializer(resultats_importes, many=True, context={'request': request})
        return Response({
            "status":"success",
            "importes": len(resultats_importes),
            "erreurs": erreurs,
            "resultats": serializer.data
        }, status=201)


class ListeResultatsView(generics.ListAPIView):
    serializer_class = ResultatConcoursSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user,'role',None) == 'ADMIN':
            return ResultatConcours.objects.all()
        return ResultatConcours.objects.filter(utilisateur=user)


# -------- CRUD Admin Candidat / Etudiant / Formulaire --------
class CandidatListCreateView(generics.ListCreateAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class EtudiantListCreateView(generics.ListCreateAPIView):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class FormulaireListCreateView(generics.ListCreateAPIView):
    queryset = Formulaire.objects.all()
    serializer_class = FormulaireSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
