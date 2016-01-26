import requests

def blacklist(blacklist, general):
    for b in blacklist.split():
        if b in general:
            return False
    return True

def dandl(tag):
    with open("blacklist.txt", "r") as blf:
        blt = blf.read()
    page = 0
    score = 0
    pjson = requests.get("http://donmai.us/posts.json?tags=" + tag + "&limit=200&page=" + str(page)).json()
    while len(pjson) > 0:
        for item in pjson:
            if blacklist(blt, item["tag_string"]):
                print(score, end="\r")
                pic = requests.get("http://donmai.us" + item["large_file_url"]).content
                filename = str(item["id"]) + "." + item["file_ext"]
                with open(filename, "wb") as fpic:
                    fpic.write(pic)
                score += 1

        page += 1
        pjson = requests.get("http://donmai.us/posts.json?tags=" + tag + "&limit=200&page=" + str(page)).json()
    

print("Loading...", end="\r")
print("-*- Danbooru Downloader 3 -*-")
print("                 python ^")
print("-----------------------------")
print("* Input some tags to begin *")
print("Alternatively, input a letter", "to do something else.", sep="\n")
print("[b] Local blacklisting")
while 1:
    thing = input(">>>")
    if thing == "b":
        blt = input("Input tags: ")
        with open("blacklist.txt", "w") as blf:
            blf.write(blt)
    else:
        dandl(thing)
