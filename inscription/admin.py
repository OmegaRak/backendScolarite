from django.contrib import admin
from .models import Concours, InscriptionConcours, ResultatConcours, Candidat, Etudiant, Formulaire

@admin.register(Concours)
class ConcoursAdmin(admin.ModelAdmin):
    list_display = ('id','nom','date_debut','date_fin','statut')
    search_fields = ('nom',)

@admin.register(InscriptionConcours)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('id','utilisateur','concours','date_inscription','statut')
    list_filter = ('statut',)

@admin.register(ResultatConcours)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ('id','concours','utilisateur','note','classement','admis')

admin.site.register(Candidat)
admin.site.register(Etudiant)
admin.site.register(Formulaire)
