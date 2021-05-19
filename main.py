import requests
from bs4 import BeautifulSoup
import downloadsongtest
import os


test = "https://open.spotify.com/playlist/7m5Iv6ZqXCkmyOlx1X5nNb" #my playlist
test = input("Insert link:\n")


r = requests.get(test)
soup = BeautifulSoup(r.text,"html.parser")
divs = soup.find("div").find_all("div")
items = BeautifulSoup(divs[3].text, "html.parser").text.split("\n")

offset = 0
for x in range(len(items)):
    if x == 0:
        destination = items[x].split("By")[0]
    if x % 2 != 0:
        items.pop(x-offset)
        offset += 1

splitting_char = "•"

songs = []
for song in items[1:]:
    s = song.strip().split(splitting_char)
    e = s[1].split(":")[0][:-1]
    s = s[0] + e
    print(s)
    songs.append(s)

#exit(0)
if not os.path.exists(destination):
    os.mkdir(destination)

for i in songs:
    song = downloadsongtest.youtube_search(downloadsongtest.ytdl, i)
    downloadsongtest.save_with_ytdl(song, destination)