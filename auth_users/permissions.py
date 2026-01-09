# ============================================
# PERMISSIONS MULTI-TENANT
# ============================================
# auth_users/permissions.py ou core/permissions.py

from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """Seul le SuperAdmin a accès"""
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'SUPERADMIN'
        )


class IsAdminUser(BasePermission):
    """Admin d'un établissement (pas SuperAdmin)"""
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'ADMIN'
            and request.user.etablissement is not None
        )


class IsSuperAdminOrAdmin(BasePermission):
    """SuperAdmin OU Admin d'établissement"""
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role in ['SUPERADMIN', 'ADMIN']
        )


class IsCandidatUser(BasePermission):
    """Utilisateur avec rôle Candidat"""
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'CANDIDAT'
        )


class IsEtudiantUser(BasePermission):
    """Utilisateur avec rôle Étudiant"""
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'ETUDIANT'
        )


class IsSameEtablissement(BasePermission):
    """
    Vérifie que l'utilisateur appartient au même établissement
    que l'objet qu'il essaie d'accéder.
    
    Usage: Ajouter après IsAdminUser pour restreindre l'accès
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'SUPERADMIN':
            return True  # SuperAdmin voit tout
        
        if not request.user.etablissement:
            return False
        
        # Déterminer l'établissement de l'objet selon son type
        obj_etablissement = None
        
        if hasattr(obj, 'etablissement'):
            obj_etablissement = obj.etablissement
        elif hasattr(obj, 'concours') and hasattr(obj.concours, 'etablissement'):
            obj_etablissement = obj.concours.etablissement
        elif hasattr(obj, 'annee_scolaire') and hasattr(obj.annee_scolaire, 'etablissement'):
            obj_etablissement = obj.annee_scolaire.etablissement
        elif hasattr(obj, 'niveau') and hasattr(obj.niveau, 'etablissement'):
            obj_etablissement = obj.niveau.etablissement
        elif hasattr(obj, 'utilisateur') and hasattr(obj.utilisateur, 'etablissement'):
            obj_etablissement = obj.utilisateur.etablissement
        
        return obj_etablissement == request.user.etablissement


# ============================================
# MIXIN POUR FILTRER PAR ÉTABLISSEMENT
# ============================================

class EtablissementFilterMixin:
    """
    Mixin pour filtrer automatiquement les querysets par établissement.
    À utiliser dans les vues.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # SuperAdmin voit tout
        if user.role == 'SUPERADMIN':
            return queryset
        
        # Admin voit son établissement
        if user.role == 'ADMIN' and user.etablissement:
            # Filtrer selon le modèle
            if hasattr(queryset.model, 'etablissement'):
                return queryset.filter(etablissement=user.etablissement)
            elif hasattr(queryset.model, 'concours'):
                return queryset.filter(concours__etablissement=user.etablissement)
            elif hasattr(queryset.model, 'annee_scolaire'):
                return queryset.filter(annee_scolaire__etablissement=user.etablissement)
            elif hasattr(queryset.model, 'niveau'):
                return queryset.filter(niveau__etablissement=user.etablissement)
            elif hasattr(queryset.model, 'utilisateur'):
                return queryset.filter(utilisateur__etablissement=user.etablissement)
        
        # Candidat/Étudiant voit ses propres données
        if hasattr(queryset.model, 'utilisateur'):
            return queryset.filter(utilisateur=user)
        
        return queryset.none()