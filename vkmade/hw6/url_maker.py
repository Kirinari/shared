base = "https://ru.wikipedia.org/wiki/500_год"
N_LINKS = 10
PATH = "url.txt"
with open(PATH, "w", encoding="utf-8") as f:
    for i in range(500, 500 + N_LINKS):
        new_url = base.replace("500", str(i))
        f.write(new_url + '\n')   
        

