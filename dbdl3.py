import requests, os, pickle

def blacklist(blacklist, general):
    for b in blacklist.split():
        if b in general:
            return False
    return True

def achievements(typeof, arg):
    """Achievements thing
typeof is an int, corresponding with the list below.
arg is what will be tested. Check list below.
    -1: Return the current dict achievement
      * arg is whatever
    0: Tag
      * arg is a string
    1: Download milestone
      * arg is an int

    Return the name of the achievement if you get an achievement, nothing if you don't"""

    if typeof == -1:
        with open("achievement.dbdl", "rb") as af:
            return pickle.load(af)
    
    with open("achievements.dbdl", "rb") as af:
        ach = pickle.load(af)

    with open("achievements.dbdl", "wb") as af:
        if typeof == 0:
            if arg == "kousaka_honoka" and ach["RAISE YOUR HONKERS"] == False:
                ach["RAISE YOUR HONKERS"] == True
                pickle.dump(ach, af)
                return "RAISE YOUR HONKERS"
        if typeof == 1:
            ach["downloaded"] += arg
            pickle.dump(arg, af)
            
            

def dandl(tag):
    """Downloading pictures from danbooru with the supplied tags
    Will return False is tag sting is empty"""  
    if len(tag) == 0:
        return False

    with open("blacklist.txt", "r") as blf:
        blt = blf.read()

#    acht = achievements(0, tag)
#    if acht != "":
#        print("* Achievement get! [{}]".format(acht))
        
    if os.path.exists(tag) == False:
        os.mkdir(tag)
    os.chdir(tag)
    
    page = 0
    score = 0
    skipped = 0
    sourcefile = {}
    pjson = requests.get("http://donmai.us/posts.json?tags=" + tag + "&page=" + str(page)).json()
    while len(pjson) > 0:
        for item in pjson:
            if blacklist(blt, item["tag_string"]):
                print(score, end="\r")
                print("http://donmai.us" + item["file_url"])
                pic = requests.get("http://donmai.us" + item["file_url"]).content
                filename = item["rating"] + "_" + str(item["id"]) + "." + item["file_ext"]
                print("{} : {}".format(score, filename), end="\r")
                with open(filename, "wb") as fpic:
                    fpic.write(pic)
                score += 1
                sourcefile[item["id"]] = item
                with open(tag + ".dbdl", "wb") as sf:
                    pickle.dump(sourcefile, sf)
            else:
                skipped += 1
        page += 1
        pjson = requests.get("http://donmai.us/posts.json?tags=" + tag + "&page=" + str(page)).json()
        
    print("Downloaded {} pictures, skipped {}".format(score, skipped))
    os.chdir("..")
#    achievements(1, score)
    print("----------------------------------------")

#---------------------

print("Loading...", end="\r")
print("-*- Danbooru Downloader 3 -*-")
print("                 python ^")
print("-----------------------------")
print("* Input some tags to begin *")
print("Alternatively, input a letter", "to do something else.", sep="\n")
#print("[a] Achievement init")
print("[b] Local blacklisting")
while 1:
    thing = input(">>>")
    if thing == "b":
        blt = input("Input tags: ")
        with open("blacklist.txt", "w") as blf:
            blf.write(blt)
#    elif thing == "a":
#        empty = {"downloaded": 0,
#                 "It's ok.": False,
#                 "RAISE YOUR HONKERS": False}
        with open("achievements.dbdl", "wb") as nf:
            pickle.dump(empty, nf)
    else:
        dandl(thing)
