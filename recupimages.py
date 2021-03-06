#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import os
import re
import shutil
import sys

## Configuration, à adapter
EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif"] # Extensions autorisées pour nos images
BACKUP_DIR = "backup" # Répertoire dans lequel on copie les fichiers d'origine avant de les modifier
BASE_URL = "http://liltools.lacherez.info" # URL de base du site d'origine pour compléter les URL relatives
IMAGE_DIR = "archives_images" # Répertoire pour les images
IMAGE_PREFIX = "/archives_images" # Chemin vers le répertoire pour les images pour les liens
## Fin de la configuration

def sans_query(url):
    """Renvoie l'url sans querystring"""
    p = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((p.scheme, p.netloc, p.path, "", "", ""))

def absolute_url(url):
    """Renvoie l'url en transformant les url relatives en url absolues"""
    p = urllib.parse.urlparse(url)
    if p.scheme:
        # L'url est absolue
        new_url = url
    else:
        # URL relative : on ajoute BASE_URL au début
        new_url = urllib.parse.urljoin(BASE_URL, url)
    return new_url

def is_image(url):
    """Vérifie que l'url correspond à une image dans un des formats autorisés
    """
    ext = os.path.splitext(url)[1].lower()
    if ext in EXTENSIONS:
        return True
    return False

def liste_images(f, liens=False):
    """Renvoie la liste des images dans le contenu de f, qui doit être du HTML.
    f est une chaîne
    liens indique si on récupère aussi les images liées (quand une image comporte un lien, souvent vers une version plus grande)
    """
    obj = BeautifulSoup(f, "html5lib")
    img = obj.find_all("img")
    images = []
    for i in img:
        url = i.get("src")
        new_src = sans_query(url)
        if is_image(new_src) and not new_src in images:
            images.append(new_src)
        if liens:
            if i.parent.name == "a":
                cible = i.parent.get("href")
                if is_image(cible) and not cible in images:
                    images.append(cible)
    return images

def chemin_image(url, dest, prefixe_http):
    """
    Renvoie le chemin d'une image, en créant les répertoires si nécessaie.
    """
    chemin_distant = urllib.parse.urlparse(url).path
    if chemin_distant[0] == "/":
        chemin = chemin_distant[1:]
    else:
        chemin = chemin_distant
    print(chemin)
    chemin_final = os.path.join(dest, chemin)
    chemin_http = os.path.join(prefixe_http, chemin)
    repertoire = os.path.split(chemin_final)[0]
    if not os.path.exists(repertoire):
        os.makedirs(repertoire)
    return (chemin_final, chemin_http)

def get_image(url, dest, prefixe_http):
    """
    Télécharge l'image à l'adresse url et l'enregistre dans le répertoire dest
    """
    if not os.path.exists(dest):
        os.makedirs(dest)
    if not os.path.isdir(dest):
        raise NotADirectoryError
    else:
        (nouveau_nom, nom_lien) = chemin_image(url, dest, prefixe_http)
        try:
            urllib.request.urlretrieve(absolute_url(url), nouveau_nom)
        except:
            sys.stderr.write("Erreur pour le fichier %s : %s\n" % (url, sys.exc_info()[0]))
    return (nouveau_nom, nom_lien)

def traite(contenu):
    images = liste_images(contenu, True)
    #print(images)
    correspondances = {}
    for i in images:
        correspondances[i] = get_image(i, IMAGE_DIR, IMAGE_PREFIX)
        #print(correspondances)
    if len(correspondances):
        pattern = re.compile('|'.join(correspondances.keys()))
        r = pattern.sub(lambda x: correspondances[x.group()][1], contenu)
        return r
    return contenu

if __name__ == '__main__':
    import sys
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    for fichier in sys.argv[1:]:
        shutil.copyfile(fichier, os.path.join(BACKUP_DIR, fichier))
        with open(fichier) as f:
            contenu = f.read()
        nouveau_contenu = traite(contenu)
        if nouveau_contenu != contenu:
            with open(fichier, "w") as f:
                f.write(nouveau_contenu)
