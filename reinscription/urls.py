from django.urls import path
from .views import (
    ReinscriptionCreateView, 
    ReinscriptionListAdminView, 
    ReinscriptionValidationView, 
    AnneeScolaireListCreateView,
    NiveauxListView,
    ResultatNiveauImportView,
    ReinscriptionListUserView,
    ResultatNiveauListView,
)

urlpatterns = [
    path('create/', ReinscriptionCreateView.as_view(), name='reinscription-create'),
    path('admin/list/', ReinscriptionListAdminView.as_view(), name='reinscription-list'),
    path('admin/valider/<int:pk>/', ReinscriptionValidationView.as_view(), name='reinscription-validate'),
    path('annees/', AnneeScolaireListCreateView.as_view(), name='annee-list-create'),
    path('niveaux/', NiveauxListView.as_view(), name='niveaux-list'),
    path('resultats-niveau/import/', ResultatNiveauImportView.as_view(), name='resultat-niveau-import'),

    # ✅ Frontend
    path('user/reinscriptions/', ReinscriptionListUserView.as_view(), name='user-reinscriptions'),
    path('resultats-niveau/', ResultatNiveauListView.as_view(), name='resultats-niveau-list'),
]
