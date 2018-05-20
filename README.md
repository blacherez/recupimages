# Utilisation
- Clonez le projet :

```bash
$ git clone https://github.com/blacherez/recupimages
```
- Installez les dépendances :

```bash
$ pip install requirements.txt
```

- Adaptez la configuration dans `recupimages.py` :
```python
## Configuration, à adapter
EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif"] # Extensions autorisées pour nos images
BACKUP_DIR = "backup" # Répertoire dans lequel on copie les fichiers d'origine avant de les modifier
BASE_URL = "http://outils.lacherez.info" # URL de base du site d'origine pour compléter les URL relatives
IMAGE_DIR = "archives_images" # Répertoire pour les images
IMAGE_PREFIX = "/archives_images" # Chemin vers le répertoire pour les images pour les liens (chemin HTTP final)
## Fin de la configuration
```

- Lancez le script avec les fichiers à modifier en arguments :

```bash
$ python recupimages.py fichier1.html fichier2.html...
```

Les images seront copiés dans le dossier spécifié par la variable `IMAGE_DIR` et les fichiers HTML seront modifiés sur place (mais la version originale est sauvegardée dans le dossier `BACKUP_DIR`).

**Attention !** Si le script est lancé plusieurs fois, les sauvegardes des fichiers HTML d'origine seront écrasées par la nouvelle version des fichiers.

# Plus d'informations sur ce script
J'ai écrit un billet expliquant un peu plus le fonctionnement de ce script sur [mon blog](https://outils.lacherez.info)
