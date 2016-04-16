import random
def randompic(tag):
    # Pics: Tous les fichiers d'un dossier
    # Exts: Tous les formats de fichier acceptés
    # Alls: Tous les fichiers avec une extension dans Exts
    pics = os.listdir(tag)
    exts = [".jpg", ".jpeg", ".png"]
    alls = []
    # Pour chaque image, ensuite pour chaque extension on regarde si c'est valable
    for a in pics:
        for b in exts:
            if b in a:
                alls.append(a)
    # Puis on en retourne un au pif
    return random.choice(alls)

    # Le code est moche et très moche mais ça marche.
