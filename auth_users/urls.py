from django.urls import path
from .views import UtilisateurRegistrationView, MyTokenObtainPairView, UtilisateurProfilView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UtilisateurRegistrationView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UtilisateurProfilView.as_view(), name='profile'),
]
