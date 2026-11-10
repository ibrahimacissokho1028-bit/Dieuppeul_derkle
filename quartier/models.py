from django.db import models


class EtapeHistoire(models.Model):
    repere = models.CharField("repère", max_length=80)
    titre = models.CharField("titre", max_length=150)
    description = models.TextField("description")
    ordre = models.PositiveIntegerField("ordre d'affichage", default=0)

    class Meta:
        ordering = ["ordre", "id"]
        verbose_name = "étape de l'histoire"
        verbose_name_plural = "étapes de l'histoire"

    def __str__(self):
        return f"{self.repere} — {self.titre}"


class Lieu(models.Model):
    class Categorie(models.TextChoices):
        MOSQUEE = "mosquee", "Mosquée"
        MARCHE = "marche", "Marché"
        ECOLE = "ecole", "École"
        SPORT = "sport", "Sport"
        CULTURE = "culture", "Culture"
        AUTRE = "autre", "Autre"

    nom = models.CharField("nom", max_length=120)
    description = models.TextField("description")
    categorie = models.CharField(
        "catégorie",
        max_length=20,
        choices=Categorie.choices,
        default=Categorie.AUTRE,
    )
    image = models.ImageField("image", upload_to="lieux/")

    class Meta:
        ordering = ["nom"]
        verbose_name = "lieu"
        verbose_name_plural = "lieux"

    def __str__(self):
        return self.nom


class Evenement(models.Model):
    titre = models.CharField("titre", max_length=150)
    description = models.TextField("description")
    date = models.DateTimeField("date et heure")
    image = models.ImageField("image", upload_to="evenements/", blank=True)

    class Meta:
        ordering = ["date"]
        verbose_name = "événement"
        verbose_name_plural = "événements"

    def __str__(self):
        return self.titre


class PhotoGalerie(models.Model):
    class Categorie(models.TextChoices):
        RUES = "rues", "Rues"
        PERSONNES = "personnes", "Personnes"
        EVENEMENTS = "evenements", "Événements"
        ARCHITECTURE = "architecture", "Architecture"

    image = models.ImageField("image", upload_to="galerie/")
    legende = models.CharField("légende", max_length=200)
    categorie = models.CharField(
        "catégorie",
        max_length=20,
        choices=Categorie.choices,
        default=Categorie.RUES,
    )

    class Meta:
        ordering = ["legende"]
        verbose_name = "photo de la galerie"
        verbose_name_plural = "photos de la galerie"

    def __str__(self):
        return self.legende


class Temoignage(models.Model):
    class Role(models.TextChoices):
        HABITANT = "habitant", "Habitant(e)"
        DIASPORA = "diaspora", "Membre de la diaspora"
        COMMERÇANT = "commercant", "Commerçant(e)"
        AUTRE = "autre", "Autre"

    nom = models.CharField("nom", max_length=120)
    role = models.CharField("rôle", max_length=20, choices=Role.choices, default=Role.HABITANT)
    citation = models.TextField("citation")

    class Meta:
        ordering = ["nom"]
        verbose_name = "témoignage"
        verbose_name_plural = "témoignages"

    def __str__(self):
        return f"{self.nom} — {self.get_role_display()}"


class MessageContact(models.Model):
    nom = models.CharField("nom", max_length=120)
    email = models.EmailField("adresse e-mail")
    message = models.TextField("message")
    date_envoi = models.DateTimeField("date d'envoi", auto_now_add=True)

    class Meta:
        ordering = ["-date_envoi"]
        verbose_name = "message de contact"
        verbose_name_plural = "messages de contact"

    def __str__(self):
        return f"{self.nom} — {self.date_envoi:%d/%m/%Y}"


class ChiffreCle(models.Model):
    libelle = models.CharField("libellé", max_length=100)
    valeur = models.PositiveIntegerField("valeur")
    icone = models.CharField(
        "icône (symbole ou emoji)",
        max_length=40,
        help_text="Exemple : ✨, 🏘️ ou un symbole court.",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "chiffre clé"
        verbose_name_plural = "chiffres clés"

    def __str__(self):
        return f"{self.libelle} : {self.valeur}"
