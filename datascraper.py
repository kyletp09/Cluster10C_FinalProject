import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from lyricsgenius import Genius
import json

# Loading Environment
load_dotenv()
token = os.getenv("GENIUS_ACCESS_TOKEN")
id = 69

# Search for all songs Made by J. Cole

genius = Genius(
    token,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)", "(Demo)", "(Acoustic)", "Freestyle", "Snippet", "Tracklist"],
    remove_section_headers=True,
    sleep_time = 1, 
    retries = 3
    )

page = 1
songs = []

while page:
    print(page)
    request = genius.artist_songs(id,
                                  sort='release_date',
                                  per_page=50,
                                  page=page)
    songs.extend(request['songs'])
    page = request['next_page']

with open('songs.json', 'w+') as file:
    json.dump(songs, file, indent=4)

#artist = genius.search_artist('J. Cole')
#artist.save_lyrics()

songs_dict = {
    "Title": [],
    "Album": [],
    "Language": [],
    "Lyrics": []
}

with open('saved_artist_lyrics_j.json', 'r') as file:
    songs = json.load(file)

for song in songs['songs']:
    songs_dict['Title'].append(song.get('title'))
    songs_dict['Album'].append(song.get('album').get('name') if song.get('album') else None)
    songs_dict['Language'].append(song.get('language'))
    songs_dict['Lyrics'].append(song.get("lyrics"))

df = pd.DataFrame(songs_dict)

df.head()

df.to_csv('j_cole.csv')