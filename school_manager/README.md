# School Manager — TP guidé 3

Projet Django autonome réalisé à partir du document « Stocker les étudiants dans
une base de données ». Le dossier du site Dieupeul Derkle reste inchangé.

Le document du TP 2 n'étant pas présent dans le dépôt, ses anciens templates ne
pouvaient pas être repris. Des templates équivalents, avec navigation, fiches,
recherche, statistiques et mise en page responsive, sont fournis ici.

## 1. Préparer l'environnement (Windows / PowerShell)

Ouvrir le dossier `school_manager` dans VS Code, puis ouvrir un terminal :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloque l'activation, autoriser les scripts uniquement dans ce
terminal puis recommencer :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Le dossier de travail doit être celui qui contient `manage.py`. Le projet
utilise la base SQLite `db.sqlite3` dans ce même dossier.

## 2. Architecture et configuration

`school_project` contient seulement la configuration Django. Les applications
ont chacune leur sujet : `pages` (accueil et présentation), `students`
(étudiants) et `teachers` (enseignants). `school_project/settings.py` déclare
ces applications, active les templates partagés du dossier `templates/`, règle
SQLite, le français et le fuseau horaire de Dakar.

`school_project/urls.py` conserve la route Django `/admin/` et délègue le reste
aux fichiers `urls.py` de chaque application. Les noms `app_name` permettent
d'écrire des liens non ambigus comme `{% url 'students:list' %}`.

Les templates utilisent `templates/base.html`, commun aux pages. Les templates
propres aux applications sont rangés dans `pages/templates/pages/`,
`students/templates/students/` et `teachers/templates/teachers/`.

## 3. Modèles et migrations

Dans `students/models.py`, `Student` décrit les champs prénom, nom, email
unique, classe, téléphone facultatif, statut actif, date de naissance
facultative et date d'inscription automatique. L'identifiant `id` est créé par
Django. `Meta.ordering` trie par nom puis prénom et `__str__` produit un nom
lisible.

Les migrations reproduisent les deux étapes demandées :

- `students/migrations/0001_initial.py` crée Student sans téléphone.
- `students/migrations/0002_student_phone.py` ajoute le téléphone facultatif.
- `teachers/migrations/0001_initial.py` crée le modèle Teacher.

Pour les vérifier ou les rejouer :

```powershell
python manage.py showmigrations
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` écrit le plan en fichiers Python ; `migrate` applique ces
plans à SQLite. Ne modifiez pas les fichiers de migration générés à la main.

## 4. Données de démonstration

Le fixture `students/fixtures/initial_data.json` reprend exactement les six
étudiants et les trois enseignants du TP. Après les migrations, chargez-les
une fois :

```powershell
python manage.py loaddata initial_data
```

Le résultat est de 6 étudiants (5 actifs et 1 inactif), 2 étudiants en L1,
et 3 enseignants. Le téléphone et la date de naissance ne sont pas renseignés
au départ. Ne rechargez pas ce fixture après avoir modifié les enregistrements :
il réinitialise ces lignes de démonstration.

## 5. Administration

`students/admin.py` configure les colonnes, les filtres par classe/activité et
la recherche ; `teachers/admin.py` expose également les enseignants.

Créer votre propre compte administrateur (le mot de passe est saisi localement
et ne doit pas être inscrit dans le code) :

```powershell
python manage.py createsuperuser
```

Lancer ensuite le site et ouvrir `/admin/` :

```powershell
python manage.py runserver
```

Connectez-vous avec les identifiants choisis pendant `createsuperuser`. Les
sections Students et Teachers permettent d'ajouter, modifier et supprimer les
enregistrements. Le doublon d'un email étudiant ou enseignant est rejeté par
`unique=True`.

## 6. URLs et comportements à vérifier

| URL | Résultat attendu |
| --- | --- |
| `/` | Accueil, total réel de 6 étudiants et 5 actifs |
| `/about/` | Présentation du projet |
| `/students/` | Les six étudiants, triés par nom |
| `/students/1/` | Fiche d'Awa Diop |
| `/students/999/` | Page 404, sans erreur serveur |
| `/students/classe/L1/` | Awa Diop et Fatou Ndiaye |
| `/students/classe/M1/` | Message « Aucun étudiant inscrit » |
| `/students/?q=di` | Awa Diop et Fatou Ndiaye ; le formulaire garde « di » |
| `/teachers/` | Mamadou Ba, Cheikh Diallo et Aïssatou Sy, triés par nom |
| `/admin/` | Administration Django après connexion |

Le filtrage par classe utilise `filter()`. Le détail utilise
`get_object_or_404()`. La recherche GET combine les champs prénom et nom avec
`Q(... ) | Q(... )`.

## 7. Tester l'ORM dans le shell Django

Dans le terminal, après avoir chargé les données :

```powershell
python manage.py shell
```

Saisir les lignes suivantes une par une :

```python
from students.models import Student
Student.objects.all()
Student.objects.count()
Student.objects.get(email="awa.diop@ecole.sn")
Student.objects.filter(classe="L1")
Student.objects.filter(active=False)
test = Student.objects.create(
    first_name="Khady",
    last_name="Gueye",
    email="khady.gueye@ecole.sn",
    classe="L1",
)
Student.objects.count()
test.classe = "L2"
test.save()
test.delete()
Student.objects.count()
exit()
```

Résultats clés : `all()` contient 6 lignes ; `count()` renvoie 6, puis 7 après
`create()`, puis 6 après `delete()` ; `get()` renvoie Awa Diop ; `filter()` pour
L1 renvoie 2 étudiants. `save()` persiste la modification de classe avant la
suppression de l'objet de test.

## 8. Vérifications automatiques

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

`check` doit afficher « System check identified no issues ». La commande de
migrations doit signaler qu'aucun changement n'est détecté.

## 9. Réponses aux dix questions de validation

1. **Pourquoi ne pas mettre les données dans le code ?** Les données changent
   souvent et doivent rester modifiables sans toucher au programme. Une base
   les conserve durablement et permet les recherches et les modifications par
   plusieurs utilisateurs.
2. **Table, ligne, colonne, clé primaire ?** Une table rassemble un type de
   données ; une ligne représente un enregistrement ; une colonne, un champ ;
   la clé primaire (`id`) identifie chaque ligne de façon unique.
3. **Qu'est-ce qu'un Model ?** Une classe Django qui décrit une table. Chaque
   attribut de champ devient une colonne ; Django fournit l'identifiant
   automatiquement.
4. **`makemigrations` et `migrate` ?** La première commande génère les fichiers
   décrivant les changements ; la seconde les applique réellement à la base.
5. **`all()`, `get()`, `filter()` ?** `all()` renvoie un QuerySet de tous les
   résultats ; `get()` renvoie un objet unique (ou lève une exception s'il est
   absent ou non unique) ; `filter()` renvoie un QuerySet de tous les résultats
   correspondants, éventuellement vide.
6. **Pourquoi `get_object_or_404()` dans une vue ?** Il convertit l'absence de
   l'objet en réponse HTTP 404 adaptée, au lieu de laisser l'exception de
   `get()` devenir une erreur serveur 500.
7. **Pourquoi les templates du TP 2 changent-ils peu ?** Les vues fournissent
   toujours un contexte avec `students` ; un QuerySet s'itère comme la liste
   précédente et ses objets exposent les mêmes attributs.
8. **Quand créer une application ?** Lorsqu'un domaine fonctionnel cohérent
   mérite d'être isolé, avec ses modèles, vues et routes : ici pages générales,
   gestion des étudiants et gestion des enseignants.
9. **`include()` et `app_name` ?** `include()` délègue les routes à une
   application ; `app_name` déclare son espace de noms. Le lien vers la liste
   des étudiants s'écrit `students:list`.
10. **Pourquoi versionner les migrations, pas `db.sqlite3` ?** Les migrations
    sont le plan reproductible de la structure. La base locale contient des
    données de développement propres à chaque utilisateur et est ignorée par
    Git.

## 10. Erreurs fréquentes

- `no such table` : exécuter `python manage.py migrate`.
- `no such column ... phone` : exécuter `makemigrations`, puis `migrate`.
- `No changes detected` alors qu'un modèle manque : vérifier `INSTALLED_APPS`
  et enregistrer `models.py`.
- `Student matching query does not exist` : vérifier les critères ; dans une
  vue, employer `get_object_or_404()`.
- `UNIQUE constraint failed` : l'email existe déjà ; choisir une adresse
  distincte.
- Modèle absent de l'admin : vérifier l'import et `@admin.register(...)`.
- `NoReverseMatch` : vérifier le nom namespacé de la route, par exemple
  `students:detail`.
- `TemplateDoesNotExist` : vérifier l'emplacement des templates et que chaque
  application figure dans `INSTALLED_APPS`.
- Mot de passe administrateur oublié :
  `python manage.py changepassword <nom_utilisateur>`.

## 11. Structure finale

```text
school_manager/
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
├── README.md
├── templates/
│   └── base.html
├── school_project/
│   ├── settings.py
│   └── urls.py
├── pages/
│   ├── templates/pages/ (home.html, about.html)
│   ├── urls.py
│   └── views.py
├── students/
│   ├── fixtures/ (initial_data.json)
│   ├── migrations/ (0001_initial.py, 0002_student_phone.py)
│   ├── static/students/style.css
│   ├── templates/students/ (student_list.html, student_detail.html)
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
└── teachers/
    ├── migrations/ (0001_initial.py)
    ├── templates/teachers/ (teacher_list.html)
    ├── admin.py
    ├── models.py
    ├── urls.py
    └── views.py
```
