import youtube_dl
import requests
import re
import os

illegal_chars = list(r'\/:*?"<>|')

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': True,
    'quiet': True,
    'no_warnings': False,
    'default_search': 'auto',
    'preferredcodec': 'mp3',
    'preferredquality': '192',
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# serach
def youtube_search(ytdl, video_name):
    # print(video_name)
    try:
        ytdl.get(video_name)
    except:
        return ytdl.extract_info(f"ytsearch: {video_name}", download=False)['entries']
    else:
        return ytdl.extract_info(video_name, download=False)['entries']

def remove_non_char(string):
    n = "".encode('utf-8')
    for char in string:
        if char in illegal_chars:
            n+=" ".encode('utf-8')
        else:
            n+=char.encode('utf-8')
    return " ".join(x.decode() for x in n.split()).encode('utf-8').decode('utf-8')

def save_song(song, destination):
    url = song["url"]
    name = remove_non_char(song["title"])
    lib = os.listdir(destination)
    if name+".mp3" in lib:
        print(f"{name} was found in {destination}")
        return
    print(f"Downloading: {name}")
    r = requests.get(url)
    with open(destination+f"/{name}.mp3", "wb") as f:
        f.write(r.content)
        f.close()


base_folder = "downloads"
def save_with_ytdl(song, destination):
    url = song['url']
    name = remove_non_char(song['title']) + ".mp3"
    lib = os.listdir(os.path.join(base_folder, destination))
    if name in lib:
        print(f"'{name}' was found in '{destination}'")
        return
    
    # create ytdl info 
    ydl_info = ytdl_format_options.copy()
    # set the output filename
    path = os.path.join(base_folder, destination, name)
    ydl_info['outtmpl'] = path
    
    # '\\%(title)s.%(ext)s'

    print(f"Downloading: {name} | To: {path}")
    with youtube_dl.YoutubeDL(ydl_info) as ydl:
        # get search results
        info_dict = ydl.extract_info(url, download=True)