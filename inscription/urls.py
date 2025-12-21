from django.urls import path
from .views import (
    ConcoursListCreateView, ConcoursRetrieveUpdateDestroyView,
    InscriptionConcoursCreateView, ListeInscriptionsView, InscriptionConcoursUpdateStatusView,
    ResultatConcoursImportView, ListeResultatsView,
    CandidatListCreateView, EtudiantListCreateView, FormulaireListCreateView, ResultatBaccalaureatImportView, 
    ResultatBaccalaureatListView
)

urlpatterns = [
    path('resultats-bac/import/', ResultatBaccalaureatImportView.as_view(), name='resultat-bac-import'),
    path('bacheliers/', ResultatBaccalaureatListView.as_view(), name='liste-bacheliers'),

    # Concours
    path('concours/', ConcoursListCreateView.as_view(), name='concours-list-create'),
    path('concours/<int:pk>/', ConcoursRetrieveUpdateDestroyView.as_view(), name='concours-rud'),

    # Inscription
    path('inscriptions/', InscriptionConcoursCreateView.as_view(), name='inscription-create'),
    path('inscriptions/list/', ListeInscriptionsView.as_view(), name='inscription-list'),
    path('inscriptions/<int:pk>/status/', InscriptionConcoursUpdateStatusView.as_view(), name='inscription-update-status'),

    # Résultats
    path('resultats/import/', ResultatConcoursImportView.as_view(), name='resultat-import'),
    path('resultats/', ListeResultatsView.as_view(), name='liste-resultats'),

    # Admin CRUD
    path('candidats/', CandidatListCreateView.as_view(), name='candidat-list-create'),
    path('etudiants/', EtudiantListCreateView.as_view(), name='etudiant-list-create'),
    path('formulaires/', FormulaireListCreateView.as_view(), name='formulaire-list-create'),
]

