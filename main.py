import requests
from bs4 import BeautifulSoup
import os
import sys

from source import youtubehandler


SPOTIFY_SONGS_DIV = 'JUa6JJNj7R_Y3i4P8YUX'
MAX_SONG_LENGTH = 60 * 10 # max 10 minutes for a song to be considered for download

class ConsoleColor:
    # non windows-terminal
    SONG_YELLOW = "\x1b[4;30;43m"
    ARTIST_BLUE = "\x1b[4;30;44m"
    NULL = "\x1b[4;30;47m"
    VOID = "\x1b[0m"

    # redefine
    # SONG_YELLOW = ""
    # ARTIST_BLUE = ""
    # NULL = ""
    # VOID = ""

class Artist:
    def __init__(self, artist_name: str, artist_profile: str):
        self.name = artist_name
        self.profile = artist_profile

class SpotifySong:
    def __init__(self, name: str, artists: list, link: str):
        self.name = name
        self.artists = artists
        self.link = link
    
    def get_song_name(self):
        return self.name
    
    def get_artists_string(self, delim=', '):
        return delim.join([a.name for a  in self.artists])


def main():
    """Handles and runs the program"""
    # get the link
    spotify_link = input("Please insert the spotify playlist you want to download:\n>")

    # request
    website = requests.get(spotify_link)
    # parse the html
    raw_html = BeautifulSoup(website.text, "html.parser")
    # find divs
    divs = raw_html.find("div", id="main")
    # find songs
    song_list = divs.find("div", class_=SPOTIFY_SONGS_DIV)
    # find div with songs
    songs_div = song_list.contents[1]
    # get the songs
    tags = songs_div.find_all("a")

    # results array
    results = []
    cache_data = ""
    for tag in tags:
        # assume that a song name will always be first :) because thats how the <a> objects are ordered on spotify app
        # get song and check certain parameters
        href = tag.get('href')
        # check if link is to artist or not
        if href.startswith('/artist'):
            # it is an artist :)
            artist = Artist(tag.text, "https://open.spotify.com" + href)
            results[-1].artists.append(artist)
        else:
            # first, we want to output some stuff :)
            if results and results[-1].artists:
                ss = results[-1]
                print(f"{ConsoleColor.VOID}[Search] Found | {ConsoleColor.SONG_YELLOW}Song: {ss.name} {ConsoleColor.NULL}|{ConsoleColor.ARTIST_BLUE} Artists: {', '.join([_artist.name for _artist in ss.artists])}{ConsoleColor.VOID}")
            # it is a song
            spotify_song = SpotifySong(tag.text, [], href)
            results.append(spotify_song)
    
    # finished checking -- tell user
    print(f"[Search] Finished: {len(results)} songs are in the playlist!")

    # check for path
    playlist_name = input("[Prompt] Where should these songs be downloaded? (All songs are stored within the \\playlists folder)\n>").split("\\")[0]
    # check if playlists folder exists
    if not os.path.exists('playlists'):
        # create the folder
        print("[Info] The `playlists` folder could not be found. Creating the folder now.")
        os.mkdir('playlists')
    print(f"[Confirm] Songs will be stored at: {os.path.abspath('playlists/' + playlist_name)}")
    if not os.path.exists('playlists/' + playlist_name):
        # create the folder
        os.mkdir('playlists/' + playlist_name)

    # now we can start downloading
    max_tries = 3
    base_folder = os.path.abspath('playlists/' + playlist_name)
    already_downloaded = set(os.listdir(base_folder))
    for _song in results:
        # we search on youtube or smth
        yt_search_string = f"{_song.get_song_name()} by {_song.get_artists_string()}"
        # no need to output search string
        # print(yt_search_string)
        for _ in range(max_tries):
            filename = f"{youtubehandler.remove_non_char(yt_search_string)}.mp3"
            if filename in already_downloaded:
                print(f"[Download] Already Downloaded Before!")
                break 
            print(f"[Download] Currently downloading: {_song.get_song_name()} by {_song.get_artists_string()}")

            finished = False
            try:
                # get potential songs
                potentials = youtubehandler.ytdl.extract_info(yt_search_string, download=False)['entries']
                
                # this should only go like 2 or 3 songs max -- max check 5
                for p in range(min(len(potentials), 5)):
                    # check for duration
                    pdata = potentials[p]
                    if pdata['duration'] > MAX_SONG_LENGTH:
                        continue
                    # if length is under limit
                    # output info
                    youtubehandler.save_with_ytdl(pdata, os.path.join(base_folder), fname=filename)
                    finished = True
                    break
            except Exception as e:
                # try again :)
                print("[Error] Failed to download, trying again! (max of 3 tries)")
                print(e)
            if finished:
                break
        
        # finished downloading
        print("Finished")

if __name__ == "__main__":
    main()