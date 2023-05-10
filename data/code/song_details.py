from http import HTTPStatus
import pandas as pd 
from urllib.parse import urlparse
globalcount = 0 

import re
import requests
import lyricsgenius
genius = lyricsgenius.Genius('27770e4c80530bfb03b80b262d1d915e')

import spotipy
from tqdm import tqdm
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

credentials = SpotifyClientCredentials(
    client_id="ef797cfd52a14c619dc1a4f0af4e1fe9",
    client_secret="e1d001de4ea6472d99f40025ebc6f3af",
)

sp = spotipy.Spotify(client_credentials_manager=credentials)

def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results["items"]
    c = 0
    while results["next"] and len(tracks) <= 99:
        # print (c)
        c += 1
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks


def get_album_tracks(playlist_id):
    results = sp.album_tracks(playlist_id)
    tracks = results["items"]
    while results["next"] and len(tracks) <= 99:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks


def getdeet(linklist):
    global countdict

    songdict = []

    for i in linklist:
        songlink = i
        # for play in tqdm(playlistlist):
        if "playlist" in songlink:

            try :
            # print (songlink," playlist")
                itemlist = get_playlist_tracks(i)

                for itemi in itemlist:

                        audiofeatures = sp.audio_features(itemi["track"]["uri"])
                        newdict1 = {
                            "name": itemi["track"]["name"],
                            "artist": itemi["track"]["album"]["artists"][0]["name"],
                        }
                        newdict2 = {**newdict1, **audiofeatures[0]}
                        songdict.append(newdict2)

            except Exception as e:
                print(e)
                countdict += 1

                    # print (itemi['track']['name'],itemi['track']['album']['artists'][0]['name'])
        elif "track" in songlink:
            # continue

            # print (songlink," track ")
            try:

                audiofeatures = sp.audio_features(songlink)
                # print (audiofeatures)
                basedicts = sp.track(songlink)
                newdict1 = {
                    "name": basedicts["name"],
                    "artist": basedicts["album"]["artists"][0]["name"],
                }
                newdict2 = {**newdict1, **audiofeatures[0]}
                songdict.append(newdict2)

            except Exception as e:
                print(e)
                countdict += 1

        elif "album" in songlink:
            # continue

            # print (songlink," album ")
            try:

                itemlist = get_album_tracks(i)
                for itemi in itemlist:
                    # try:
                    # print(itemi)

                    audiofeatures = sp.audio_features(itemi["uri"])
                    newdict1 = {
                        "name": itemi["name"],
                        "artist": itemi["artists"][0]["name"],
                    }
                    newdict2 = {**newdict1, **audiofeatures[0]}
                    songdict.append(newdict2)

            except Exception as e:
                print(e)
                countdict += 1

        else:
            pass
            # print ('='*80)
            # print (songlink," album ")

        return songdict



def scrape(trackname, artistname):
    cnt = 0
    while 1:
        try:
            song = genius.search_song(trackname, artistname)
            return song.lyrics
            break
        except:
            cnt += 1
            if cnt == 5:
                print(trackname + " " + artistname + " Not present in Genius")
                return ""
            continue


biglyriclist = []
countdict = 0
import json

biglist =  pd.read_csv('final_songs.csv')

final_list  = []

bigc = 0
for index,value in tqdm(biglist.iterrows()):
    dicval = value
    bigc += 1
    von = 0 
    name = dicval["track_name"]
    artist = dicval["artist_name"]
    name=re.sub("\(.*?\)","()",name)
    name = name.replace('(','').replace(')','')
    lyrics = scrape(name, artist)
    lyrics = lyrics.split('\n')[1:]
    lyrics = '. '.join(lyrics)
    dicval['lyrics'] = lyrics
    if lyrics == "":
        globalcount += 1
    final_list.append(dicval)

findf = pd.DataFrame(final_list)

print (globalcount)
findf.to_csv('with_lyr.csv')
