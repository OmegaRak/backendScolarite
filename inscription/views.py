from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
import pandas as pd
from django.conf import settings
from django.db import transaction
from .emails import notifier_admission
from django.apps import apps
from .models import Concours, InscriptionConcours, ResultatConcours, Candidat, Etudiant, Formulaire, ResultatBaccalaureat
from .serializers import (
    ConcoursSerializer, InscriptionConcoursSerializer, ResultatConcoursSerializer,
    CandidatSerializer, EtudiantSerializer, FormulaireSerializer, ResultatBaccalaureatSerializer
)
from .permissions import IsAdminUser, IsCandidatUser


class ResultatBaccalaureatImportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Vérifier le rôle ADMIN
        if getattr(request.user, 'role', None) != 'ADMIN':
            return Response({"error": "Accès refusé"}, status=403)

        # Vérifier si un fichier est envoyé
        if "fichier" not in request.FILES:
            return Response({"error": "Envoyer un fichier Excel/CSV via 'fichier'."}, status=400)

        fichier = request.FILES["fichier"]

        # Lecture du fichier CSV ou Excel
        try:
            if fichier.name.lower().endswith(".csv"):
                df = pd.read_csv(fichier)
            else:
                df = pd.read_excel(fichier)
        except Exception as e:
            return Response({"error": f"Impossible de lire le fichier : {str(e)}"}, status=400)

        # Colonnes obligatoires
        required_columns = ["numero_inscription", "nom", "prenom", "status", "annee_scolaire"]
        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Colonne manquante : {col}"}, status=400)

        resultats_ok = []
        erreurs = []

        # Parcours des lignes
        for index, row in df.iterrows():
            numero = str(row["numero_inscription"]).strip()
            nom = str(row["nom"]).strip()
            prenom = str(row["prenom"]).strip()
            status_admis = str(row["status"]).strip().upper()
            annee = str(row["annee_scolaire"]).strip()

            admis = status_admis == "ADMIS"

            try:
                # Update si numero_inscription existe, sinon création
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
                erreurs.append(f"Ligne {index + 2} : {str(e)}")  # +2 pour tenir compte de l'entête CSV/Excel

        # Sérialisation des résultats importés
        serializer = ResultatBaccalaureatSerializer(resultats_ok, many=True)

        return Response({
            "status": "success",
            "importes": len(resultats_ok),
            "erreurs": erreurs,
            "resultats": serializer.data
        }, status=201)

        
class ResultatBaccalaureatListView(generics.ListAPIView):
    """
    Liste tous les bacheliers importés (admin ou utilisateur connecté)
    """
    serializer_class = ResultatBaccalaureatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ResultatBaccalaureat.objects.all().order_by('-annee_scolaire')

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
    Validation automatique : vérifie si le candidat est admis au baccalauréat
    avant de permettre l'inscription.
    """
    serializer_class = InscriptionConcoursSerializer
    permission_classes = [IsAuthenticated, IsCandidatUser]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        utilisateur = request.user
        concours_id = request.data.get('concours')
        justificatif = request.data.get('justificatif_paiement', None)
        numero_inscription = request.data.get('numero_inscription', None)  # numéro bac

        if not concours_id:
            return Response({"error": "Le champ 'concours' est obligatoire."}, status=400)
        if not numero_inscription:
            return Response({"error": "Le numéro d'inscription au bac est obligatoire."}, status=400)

        # Vérification du concours
        try:
            concours = Concours.objects.get(pk=concours_id)
        except Concours.DoesNotExist:
            return Response({"error": "Concours introuvable."}, status=404)

        # Vérification du bac : doit être admis
        bac_result = ResultatBaccalaureat.objects.filter(
            numero_inscription=numero_inscription,
            admis=True
        ).first()

        if not bac_result:
            return Response({
                "error": "Inscription impossible : vous devez être admis au baccalauréat."
            }, status=400)

        # Création ou mise à jour de l'inscription
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
        print("🚀 IMPORT RESULTATS DÉMARRÉ")

        if "fichier" not in request.FILES:
            return Response({"error": "Fichier manquant"}, status=400)

        fichier = request.FILES["fichier"]

        try:
            df = pd.read_csv(fichier) if fichier.name.endswith(".csv") else pd.read_excel(fichier)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        print("📄 Colonnes :", df.columns)

        Utilisateur = apps.get_model(settings.AUTH_USER_MODEL)

        resultats = []
        erreurs = []

        for index, row in df.iterrows():
            print(f"\n📌 LIGNE {index + 2}")

            concours_nom = str(row.get("concours")).strip()
            nom = str(row.get("nom")).strip()
            prenom = str(row.get("prenom")).strip()
            email = str(row.get("email", "")).strip()

            try:
                note = float(row.get("note"))
            except:
                erreurs.append(f"Ligne {index+2} : note invalide")
                continue

            concours = Concours.objects.filter(nom__iexact=concours_nom).first()
            if not concours:
                erreurs.append(f"Ligne {index+2} : concours introuvable")
                continue

            # 🔎 RECHERCHE UTILISATEUR ROBUSTE
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

            print("👤 Utilisateur :", utilisateur.email)

            admis = note >= (concours.note_deliberation or 0)
            print("🎯 ADMIs :", admis)

            resultat, _ = ResultatConcours.objects.update_or_create(
                concours=concours,
                utilisateur=utilisateur,
                defaults={
                    "note": note,
                    "admis": admis,
                    "classement": row.get("classement")
                }
            )

            # 🎓 Passage candidat → étudiant
            if admis and getattr(utilisateur, "role", None) != "ADMIN":
                utilisateur.role = "ETUDIANT"
                utilisateur.save(update_fields=["role"])

                candidat = getattr(utilisateur, "candidat_profile", None)
                if candidat and not hasattr(candidat, "etudiant_profile"):
                    Etudiant.objects.create(
                        candidat=candidat,
                        matricule=f"{concours.id:03d}-{utilisateur.id:04d}"
                    )

            # 📧 ENVOI MAIL
            try:
                print("📧 ENVOI MAIL...")
                notifier_admission(utilisateur, concours, admis)
                print("✅ MAIL OK")
            except Exception as e:
                print("❌ ERREUR MAIL :", e)
                erreurs.append(f"Ligne {index+2} : erreur mail")

            resultats.append(resultat)

        serializer = ResultatConcoursSerializer(resultats, many=True, context={"request": request})

        return Response({
            "status": "success",
            "importes": len(resultats),
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
