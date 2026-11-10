from django.contrib import admin

from .models import (
    ChiffreCle,
    EtapeHistoire,
    Evenement,
    Lieu,
    MessageContact,
    PhotoGalerie,
    Temoignage,
)


@admin.register(EtapeHistoire)
class EtapeHistoireAdmin(admin.ModelAdmin):
    list_display = ("repere", "titre", "ordre")
    list_editable = ("ordre",)
    search_fields = ("repere", "titre", "description")
    ordering = ("ordre",)


@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    list_display = ("nom", "categorie")
    list_filter = ("categorie",)
    search_fields = ("nom", "description")


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ("titre", "date")
    list_filter = ("date",)
    search_fields = ("titre", "description")
    date_hierarchy = "date"


@admin.register(PhotoGalerie)
class PhotoGalerieAdmin(admin.ModelAdmin):
    list_display = ("legende", "categorie")
    list_filter = ("categorie",)
    search_fields = ("legende",)


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ("nom", "role")
    list_filter = ("role",)
    search_fields = ("nom", "citation")


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "date_envoi")
    search_fields = ("nom", "email", "message")
    list_filter = ("date_envoi",)
    readonly_fields = ("nom", "email", "message", "date_envoi")

    def has_add_permission(self, request):
        return False


@admin.register(ChiffreCle)
class ChiffreCleAdmin(admin.ModelAdmin):
    list_display = ("libelle", "valeur", "icone")
    search_fields = ("libelle",)
