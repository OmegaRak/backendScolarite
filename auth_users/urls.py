from django.urls import path
from .views import (
    UtilisateurRegistrationView, 
    MyTokenObtainPairView, 
    UtilisateurProfilView,
    EtablissementListCreateView,
    EtablissementDetailView,
    AssignAdminToEtablissementView,
    RevokeAdminView,
    ListeAdminsView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth classique
    path('register/', UtilisateurRegistrationView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UtilisateurProfilView.as_view(), name='profile'),
    
    # ✅ NOUVEAU : Gestion établissements (SuperAdmin)
    path('etablissements/', EtablissementListCreateView.as_view(), name='etablissement-list-create'),
    path('etablissements/<int:pk>/', EtablissementDetailView.as_view(), name='etablissement-detail'),
    
    # ✅ NOUVEAU : Assignation admins (SuperAdmin)
    path('assign-admin/', AssignAdminToEtablissementView.as_view(), name='assign-admin'),
    path('revoke-admin/', RevokeAdminView.as_view(), name='revoke-admin'),
    path('admins/', ListeAdminsView.as_view(), name='liste-admins'),
]