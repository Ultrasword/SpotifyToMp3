import requests
from bs4 import BeautifulSoup
import downloadsongtest
import os
import sys


# test = "https://open.spotify.com/playlist/7m5Iv6ZqXCkmyOlx1X5nNb" #my playlist
# test = input("Insert link:\n")
# test = "https://open.spotify.com/playlist/1rqAXuMEvnWgdlYRiTBOa1?si=8d799a71541e4646"
# test = 'https://open.spotify.com/playlist/5iohaZU2LgOc7fSlEMvblz?si=30a4d2173eec4d07'
test = "https://open.spotify.com/playlist/7vEZBpl2wedPF5lZSmm9Ms?si=0307077798ae4104" # hype

r = requests.get(test)
soup = BeautifulSoup(r.text,"html.parser")
divs = soup.find("div").find_all("div")
nextstep = soup.find("body").find("div", id="main") # find the main div containig all the songs
mainContainer = nextstep.find("div").find("div").find_all("div")[3]   # is the third div and find main-view-container div
# print(mainContainer.prettify()[:500])
prevSong = mainContainer.find("div", class_="JUa6JJNj7R_Y3i4P8YUX").find_all("div")[3] # find the weird class that stores all the spotify song objects
songs = prevSong.find_all("a")

# make a parser that can loop through each and check if it is a writer name or a song name
# song name is a class object while author name is href
# for i in range(0, len(songs), 3):
#     # print(songs[i])
#     # print(songs[i+1])
#     # print(songs[i+2])
#     name = songs[i].text
#     print(name)

result = []
songname = None
i = 0
string = None
authors = []
while i < len(songs):
    string = songs[i].prettify()
    if string[3] == "c":
        # if aauthors is not empty, then output hte data and clear
        if authors:
            result.append([songname, authors.copy()])
            authors.clear()
        # it is a class object and thus a song
        songname = songs[i].text
        i += 1
        continue
    # if not class object
    # chekc if author
    elif string[3] == 'h':
        # it is an author
        authors.append(songs[i].text)
        i += 1
        continue
    else:
        print(songs[i])
else:
    result.append([songname, authors])
del songname
del authors

# for i in result:
#     print(i)



destination = input("Playlist name?: \t")
if not os.path.exists(destination):
    os.mkdir(destination)
ee = False
if input("Should I continuously attempt a failed attempt?:\t").lower().startswith('y'):
    ee = True

for songblock in result:
    # all the songs are by title and by authors
    # create search string
    search = f"{songblock[0]} by " + " ".join(songblock[1])
    print(search)
    # download search
    trying = True
    while trying:
        try:
            song = downloadsongtest.youtube_search(downloadsongtest.ytdl, search)
            # continue
            downloadsongtest.save_with_ytdl(song, destination)
            trying= False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            trying = False
            print("Failed to download `" + songblock[0] + "`\t Trying again!")
            if ee:
                break

exit()

for i in songs:
    i = i.split("     ")
    i = i[1] + " " + i[0]
    
    trying = True
    while trying:
        try:
            song = downloadsongtest.youtube_search(downloadsongtest.ytdl, i)
            # continue
            downloadsongtest.save_with_ytdl(song, destination)
            trying = False
        except:
            print("Error occured, trying again!")
