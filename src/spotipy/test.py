import spotipy
from spotipy.oauth2 import SpotifyOAuth
sp = None #Before initializing spotipy
#Connect
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="#######",
        client_secret="#######",
        redirect_uri="http://localhost:8888/callback",
        scope="user-library-read"
    ))
except Exception as e:
    print(f"Cannot connect to spotify API: {e}")
print("Connected!")

#Fetch and print the user's saved tracks
try:
    results = sp.current_user_saved_tracks() #Get liked songs etc
    for i, item in enumerate(results['items']):
        track = item['track'] #Each item has metadata and we're only accessing track info
        print(f"{i + 1}. {track['name']} by {track['artists'][0]['name']}") #Print track info
except:
    print("Can't fetch user's songs")
