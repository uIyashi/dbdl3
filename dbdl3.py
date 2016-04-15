import requests, os, pickle

# Now with 300% more comments

def blacklist(blacklist, general):
    # Cette fonction renvoie False si elle trouve un des mots de
    # la liste blacklist dans le string general.
    # Utilisé pour le local blacklist. Vu que danbooru accepte que deux
    # tags bah y'a ça pour compenser.
    for b in blacklist.split():
        if b in general:
            return False
    return True

def localtag(tag, general):
    # C'est l'inverse de blacklist. J'aurai pu nommer la liste tag en
    # whitelist mais sur le coup voila quoi. general c'est un string.
    for t in tag.split():
        if t not in general:
            return False
    return True

def printsauces(datas):
    # Ça sert a afficher des infos de base sur les images. Ça implique
    # que le fichier des sources existe mais normalement, il existe.
    # 
    # C'est une légende cependant.
    #
    # datas c'est un dict je crois. POURQUOI JE CROIS C'EST UN DICT.
    print("Artist: " + datas["tag_string_artist"])
    print("ID    : " + str(datas["id"]))
    print("Pixiv : " + str(datas["pixiv_id"]))
    if "pixiv" in datas["source"]:
        source = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + source.split("/")[-1].split("_")[0].split(".")[0]
        print("Source: " + source)
    else:
        print("Source: " + datas["source"])
    print("Tags  : " + datas["tag_string"])
    print("Chars : " + datas["tag_string_character"])

def sauces(folder):
    # Pourquoi j'ai fait deux fonctions alors qu'une aurait suffi.
    # Bref. Folder c'est un string et idéalement un nom de dossier.
    # Vu que NORMALEMENT les noms de fichier de sources est le même
    # que le nom du dossier lui même, devrait pas y avoir de problème
    os.chdir(folder)
    with open(folder+".dbdl", "rb") as sourcefile:
        sdic = pickle.load(sourcefile)
        # Charge le fichier de source.
        # Si le dossier existe pas, ou le fichier lui même, ça crashe mdr.

    print("Input the ID of the picture")
    print("eg: s_420123.png > 420123")
    print("Input something else to get bak\n")

    while 1: # INFINITE POWE--
        pid = input(">>> ")
        try:
            pid = int(pid)
            printsauces(sdic[pid])
        except ValueError: # Si t'as entré autre chose qu'un int
            return 0 # Quitte la fonction
        except KeyError: # Si t'as entré un numéro d'image qui existe pas
            print("Not found :(")
            pid = 0 # On recommence a demander.

    


def dandl(tag, local):
    """Downloading pictures from danbooru with the supplied tags
    Will return False is tag sting is empty""" 
    # Plus ou moins.
    # tag c'est les tags qu'on envoie a danbooru. Si y'en as plus de deux ça va pas
    # Je suis une feignasse de pas avoir codé ça mais ça se fait facilement.
    
    # A vrai dire, comment on entre les tags c'est selon les normes de GET/POST. Faut
    # mettre "+" en séparateur des deux tags. Je suis une feignasse.
    # Si tu vois pas ce que je veux dire, regarde l'url
    # http://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=minami_kotori+sonoda_umi+&ms=1
    # Les deux tags (minami_kotori et sonoda_umi) sont séparés par +. c'est facilement
    # codable ( "....".split("+") ) mais j'ai eu la flemme de le faire BREEEEEEEF.
    
    # Si la liste des tags est vide (t'as rien mis) ça renvoie False.
    # Censé arrêter la fonction. Va pas dl tout danbooru enfin.
    if len(tag) == 0:
        return False
    
    # Regarde si blacklist.txt existe
    # C'est la liste des tags blacklistés par défault. A mettre 
    # dans un fichier txt tout con. Ou alors au menu faut entrer "b" et 
    # entrer les tags que tu veux pas voir. Utilisé avec la fonction blacklist()
    if os.path.exists("blacklist.txt"):
        with open("blacklist.txt", "r") as blf:
            blt = blf.read()
    
    # Si le dossier du/des tags n'existe pas, on le crée. Puis, on rentre dedans.
    if os.path.exists(tag) == False:
        os.mkdir(tag)
    os.chdir(tag)
    
    # btw, je suis terriblement désolé de pas utiliser "".format(). Je savais pas que ça existait avant.
    # teehee
    
    # Page: C'est le numéro de page
    # Score: C'est le nombre d'images qu'on a dl avec succès
    # Skipped: C'est le nombre d'images qu'on a PAS dl. A cause du blacklist ou des tags locaux.
    page = 0
    score = 0
    skipped = 0
    sourcefile = {}
    
    # On dl une première page d'images. Ca servira pour voir si il exite des images au moins.
    pjson = requests.get("http://donmai.us/posts.json?tags=" + tag + "&page=" + str(page)).json()
    
    print("Downloaded / Skipped")
    
    # Si y'a au moins une image...
    while len(pjson) > 0:
        
        # Pour chaque "image"...
        for item in pjson:
            # Si il n'y a pas de tags blacklistés ET que il y a les tags locaux (les deuxièmes tags que tu peux mettre) dans la liste
            # des tags généraux, on dl. Si compliqué et pourtant si simple.
            if blacklist(blt, item["tag_string"]) and localtag(local, item["tag_string"]) and ("file_url" in item):
                # Les données de l'image en elle même et son nom de fichier
                # <Rating>_<id de l'image>.<format>
                # Exemple: http://danbooru.donmai.us/posts/2331148 donnera s_2331148.jpg
                pic = requests.get("http://donmai.us" + item["file_url"]).content
                filename = item["rating"] + "_" + str(item["id"]) + "." + item["file_ext"]
                
                # On affiche la progression parce que tout le monde adore voir que ça marche
                print("{}/{}: {}".format(score, skipped, filename), end="\r")
                
                # On écrit l'image dans le fichier de l'image (duh)
                with open(filename, "wb") as fpic:
                    fpic.write(pic)
                
                # azy on a dl une image poussvert
                score += 1
                
                # Pour une obscure raison des fois le programme n'arrive pas a écrire les datas de l'image (les tags, l'artiste
                # la source...) dans le fichier. Ça arrive du coup y'a ça pour éviter que ça crashe pour rien
                try:
                    sourcefile[item["id"]] = item
                    with open(tag + ".dbdl", "wb") as sf:
                        pickle.dump(sourcefile, sf)
                except:
                    pass
            
            # Si l'image a un tag blacklisté ou un tag supplémentaire qui n'est pas dans la liste des tags, on passe cette image.
            else:
                skipped += 1
        
        # Une fois la page fini, on en prend une autre. Rinse and repeat
        page += 1
        pjson = requests.get("http://donmai.us/posts.json?tags=" + tag + "&page=" + str(page)).json()
    
    # Quand on a fini, on affiche le rapport. Admirez le .format().
    print("Downloaded {} pictures, skipped {}".format(score, skipped))
    os.chdir("..")
    print("----------------------------------------")

#---------------------

print("Loading...", end="\r")
print("-*- Danbooru Downloader 3 -*-")
print("                 python ^")
print("-----------------------------")
print("* Input some tags to begin *")
print("Alternatively, input a letter", "to do something else.", sep="\n")
print("[b] Local blacklisting")
print("[s] Info and sources")

# Entrons des tags.
while 1:
    thing = input(">>>")
    if thing == "b":
        # Si tu veux pas voir de bites, entre "penis" en tags blacklistés.
        # Aucune image avec "penis" comme tag ne sera dl. Pratique quand
        # tu veux dl des images de best idolu mais que tu veux pas 
        # voir de mecs sans visages violer la pureté de nos idoles.
        #
        # Idols are for yuri, they belongs to each other.
        blt = input("Input tags: ")
        with open("blacklist.txt", "w") as blf:
            blf.write(blt)
    
    elif thing == "s":
        # Pour afficher les infos d'une image. D'abord on rentre le nom de dossier,
        # Ensuite on rentre dans la foncion sauces,
        # Dedans on demande un id d'image,
        # Puis on affiche. SIMPLE HEIN.
        print("Enter a folder name")
        sltskyneo = input(">>> ")
        sauces(sltskyneo)
        
    else:
        # C'est après avoir entré des tags "locaux" (qui ne seront pas
        # envoyés a danbooru) que l'on va dl seulement.
        # A noter que les tags locaux ne servent qu'a enlever des images.
        # Exemple: Vu que tu peux pas demander "ayase_eli + toujou_nozomi + yuri", bah
        # tu demandes juste eli et nozomi puis tu mets yuri en tag local. Et sonic boum.
        local = input("Local tags:")
        dandl(thing, local)

# Faut que j'arrête de parler yuri au boulot.
