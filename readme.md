# Installation

Suivez ces étapes pour configurer et exécuter le projet sur votre machine locale.

## Prérequis

Assurez-vous d'avoir les outils suivants installés sur votre machine :

- **[Python 3.7+](https://www.python.org/downloads/)**
- **[Node.js et npm](https://www.npmjs.com/)**
- **[git](https://git-scm.com/)**

## Étapes

### 1. Cloner le dépôt

Clonez le dépôt et accédez au dossier du projet :

```bash
git clone https://github.com/rayankad01/massar.git
cd massar
```

### 2. Configuration du projet

Installez les dépendances Python nécessaires :

```bash

pip install cryptography secrets subprocess sys time
```

Ensuite, exécutez le fichier `setup.py` pour installer les autres dépendances et configurer le projet. Ce fichier crée l'environnement virtuel et prépare le projet pour l'exécution.

```bash

python setup.py
```

Si l'installation réussit, vous pouvez supprimer ce fichier `setup.py`.

### 3. Activation de l'environnement virtuel

#### Sur MacOS :
```bash
source .env/bin/activate
```

#### Sur Windows :
- **Avec PowerShell** :
  ```bash
  .env/Scripts/Activate.ps1
  ```

- **Avec Command Prompt (cmd)** :
  ```bash
  .env/Scripts/Activate.bat
  ```

### 4. Exécution du projet

Une fois l'environnement virtuel activé, lancez le serveur Django avec la commande suivante :

```bash
python manage.py runserver
```

Si vous souhaitez également personnaliser le style en temps réel avec TailwindCSS, vous devez exécuter le serveur Tailwind en parallèle :

```bash
python3 manage.py tailwind start
```

### 5. Problèmes avec TailwindCSS

Si vous rencontrez des problèmes d'affichage avec TailwindCSS, il est possible que la configuration doive être mise à jour. Pour cela, accédez au fichier `theme/static_src/tailwind.config.js` et remplacez son contenu par ce code :

```js
module.exports = {
  content: [
    // Fichiers de templates Django
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
```

Cela permettra à TailwindCSS de trouver et appliquer les classes dans les fichiers HTML.

## Structure du projet

Voici la structure générale du projet pour vous aider à vous y retrouver :

```
.
├── .env                 # Variables d'environnement
├── auths/               # Modules relatifs à l'authentification
├── info/                # Modules d'informations et utilitaires
├── massar/              # Logique principale de l'application
├── node_modules/        # Dépendances Node.js
├── scores/              # Modules relatifs aux scores
├── static/              # Fichiers statiques (CSS, JS, images, etc.)
├── templates/           # Templates HTML
├── theme/               # Thème TailwindCSS
├── manage.py            # Script de gestion Django
├── requirements.txt     # Dépendances Python
├── package.json         # Dépendances Node.js
├── tailwind.config.js   # Configuration de TailwindCSS
└── db.sqlite3           # Base de données SQLite (uniquement pour le développement)
```

## Variables d'environnement

Le fichier `.env` est généré automatiquement lors de l'exécution de `setup.py` et contient les variables suivantes :

```
DEBUG=True
ENCRYPTION_KEY=<votre_clé_de_chiffrement>
DJANGO_SECRET_KEY=<votre_clé_secrète_django>
```

Veillez à ne pas partager ce fichier `.env` car il contient des informations sensibles.

# Contributions

Afin de maintenir la cohérence et la qualité du code, nous demandons à tous les contributeurs de suivre les règles suivantes :

## 1. Utilisation de la langue

- **Langue principale** : Le projet utilise **le français** comme langue principale pour la documentation et les messages d'engagement. Même si le code peut être écrit en anglais, tout le reste (y compris les messages de commit, les issues, etc.) doit être en français.
  
- **Clarté** : Assurez-vous que le code, les commentaires et la documentation sont clairs et compréhensibles. Si vous devez ajouter des commentaires ou des descriptions, soyez concis et précis.

## 2. Style de codage
Nous utilisons des conventions de style pour rendre le code lisible et uniforme.
### Nouvelle norme de contribution
Nous avons récemment introduit un certain nombre de nouvelles règles de codage et de style afin d'assurer la cohérence et la qualité du code dans ce projet. Ces règles incluent, entre autres, l'indentation à **4 espaces** par niveau, l'utilisation de noms de variables explicites, et l'adhérence à des conventions spécifiques pour chaque langage (Python, JavaScript, CSS, etc.).

Nous comprenons que ces règles peuvent ne pas être immédiatement respectées dans toutes les parties du code, car elles sont nouvelles. Cependant, si vous remarquez du code qui ne suit pas ces normes, nous vous encourageons vivement à apporter les modifications nécessaires lors de vos contributions. Cela permettra de maintenir une base de code propre et cohérente pour tous les contributeurs.

Merci pour votre compréhension et pour votre aide afin de respecter ces nouvelles directives dans l'ensemble du projet !



### Python (PEP 8)
- Utilisez **PEP 8**, qui est le guide de style officiel pour Python. Cela inclut des règles concernant l'indentation, la longueur des lignes (limitez-les à 79 caractères), et les espaces blancs.
- Utilisez des noms de variables explicites en **snake_case** (par exemple, `ma_variable`).
- Les classes doivent être en **CamelCase** (par exemple, `MaClasse`).
- N'oubliez pas d'ajouter des commentaires pertinents pour expliquer les parties complexes du code.
- **Indentation** : Utilisez des **espaces (4 espaces par niveau d'indentation)** au lieu des tabulations pour l'indentation. C'est une norme recommandée par PEP 8.
  
### JavaScript (Airbnb Style Guide)
- Pour tout code JavaScript (y compris le code TailwindCSS ou les scripts personnalisés), nous suivons le [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).
- Cela inclut l'utilisation des `const` et `let` au lieu de `var`, la mise en place de fonctions fléchées (`() => {}`) et l'utilisation des `template literals` pour les chaînes de caractères.

### CSS / TailwindCSS
- Utilisez **TailwindCSS** pour le style, et évitez d'écrire du CSS personnalisé à moins que ce ne soit absolument nécessaire.
- Lorsque vous utilisez Tailwind, assurez-vous de bien organiser les classes en suivant l'ordre habituel (par exemple : `position`, `display`, `box-sizing`, `color`, `background`, `spacing`, etc.).

## 3. Processus de contribution

### 1. Forker le dépôt
   - Commencez par forker le projet sur GitHub.
   - Clonez votre fork localement en utilisant `git clone https://github.com/rayankad01/massar.git`.

### 2. Créer une branche
   - Créez une branche distincte pour vos modifications, en suivant cette convention de nommage :
     - `feature/<description-en-minuscules>` pour les nouvelles fonctionnalités.
     - `bugfix/<description-en-minuscules>` pour les corrections de bugs.
     - `docs/<description-en-minuscules>` pour les mises à jour de documentation.
   - Exemple : `feature/ajout-fonctionnalite-de-recherche`.

### 3. Effectuer les modifications
   - Apportez les modifications nécessaires dans votre branche.
   - Assurez-vous que votre code fonctionne comme prévu, en utilisant des tests automatisés ou manuels si nécessaire.
   - Ajoutez des commentaires ou des explications si le code est complexe ou non intuitif.

### 4. Effectuer des commits
   - Effectuez des commits clairs et descriptifs. Utilisez la commande suivante pour effectuer un commit :
   
     ```bash
     git commit -m "Description courte et précise de votre modification"
     ```

   - Si vous avez effectué plusieurs modifications dans un même commit, veillez à les décrire précisément.

   - **Exemple de message de commit** :  
     `Ajout d'une fonction de filtrage des résultats de recherche`.

### 5. Pousser votre branche
   - Une fois vos modifications terminées et validées, poussez-les vers votre fork :
   
     ```bash
     git push origin <nom-de-votre-branche>
     ```

### 6. Soumettre une Pull Request
   - Accédez à votre dépôt sur GitHub et soumettez une **Pull Request** (PR) vers la branche `master` du dépôt principal.
   - Dans la description de la PR, expliquez brièvement ce que vous avez modifié, pourquoi, et s'il y a des éléments à vérifier spécifiquement.

### 7. Revue de code
   - Un membre de l'équipe examinera votre PR. Si des modifications sont nécessaires, il vous fournira des retours.
   - Une fois la PR validée, elle sera fusionnée dans la branche principale.

## 4. Tests

- Avant de soumettre une PR, assurez-vous que le code respecte les tests existants et en ajoutez de nouveaux si nécessaire.
- Si vous avez modifié une fonctionnalité importante, rédigez des tests pour vérifier son bon fonctionnement.
- Utilisez `pytest` pour les tests Python et `jest` ou des outils similaires pour les tests JavaScript.

## 5. Éviter les conflits

Avant de soumettre une PR, assurez-vous que votre branche est à jour avec la branche principale (`master`).

```bash
git fetch origin
git checkout main
git pull origin master
git checkout <votre-branche>
git rebase main
```

