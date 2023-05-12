from bs4 import BeautifulSoup
import requests
import sys
import spotipy
import spotipy.util as util

# gather source info

# source = requests.get(sys.argv[2]).text

source = requests.get(input("Enter setlist.fm link: ")).text

soup = BeautifulSoup(source, 'lxml')

# title from setlist.fm

setlist_title = soup.h1.text

# date of set for playlist title

day = soup.find('span', class_ = "day").text
month = soup.find('span', class_ = "month").text
year = soup.find('span', class_ = "year").text

date = f'{day} {month} {year}' 

#title for Spotify playist

playlist_title = f'{setlist_title} - {date}'
playlist_title = playlist_title.replace('\n', ' ').strip()

# create list of artists
search_data = [] 
# setlist_artist = []

for search in soup.find_all('a', class_ = "songLabel"):
	artist = search.get('title').split('by ')[1]
	song = search.text
	search_data.append(f'{artist} {song}')

# set up Spotipy

scope = 'playlist-modify-public'
# username = sys.argv[1] # enter username after calling script in terminal
username = input("Enter Spotify username: ")
token = util.prompt_for_user_token(username,scope) #Follow Directions in Console
sp = spotipy.Spotify(auth=token)

# create playist

sp.user_playlist_create(user=username, name = playlist_title, public = True, description = '')


playlist_id = ''
playlists = sp.user_playlists(username)
playlists = playlists['items']
for playlist in playlists:  
        if playlist['name'] == playlist_title:
            playlist_id += playlist['id']

track_ids = []

for song in search_data:
	track_id = sp.search(q=song, limit=1, type='track')
	if track_id['tracks']['items'] == []:
		continue
	track_id = track_id['tracks']['items'][0]['id']
	# print(track_id)
	track_ids.append(track_id)


sp.user_playlist_add_tracks(user = username, playlist_id = playlist_id, tracks = track_ids)

print('Complete')



