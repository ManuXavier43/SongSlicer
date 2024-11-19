import spotipy, os #os for client secrets
import requests #Needed for fetching previews of songs
from dotenv import load_dotenv#Load environment variables

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth #Needed to connect to account
#Spotipy Connector class
class SpotipyClient:
    def __init__(self):
        self.sp = None
    def connectToSpotipy(self):
        #Connect to Spotify API
        try:
            load_dotenv()
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_SECRET"),
                redirect_uri="http://localhost:8888/callback",
                scope="user-library-read user-modify-playback-state user-read-playback-state"
            ))
            print("Connected!")
        except Exception as e:
            print(f"Cannot connect to Spotify API: {e}")
    def loadSampleSong(self):
        query = input("Enter an artist to search: ")
        search_result = self.sp.search(q={query}, limit=1)
        #Search an artist and cycle through their previews
        artist_uri = search_result['tracks']['items'][0]['artists'][0]['uri']
        tracks = self.sp.artist_top_tracks(artist_uri, country='US')
        for track in tracks['tracks'][:5]:
            print('track    : ' + track['name'])
            print('audio    : ' + track['preview_url'])
            preview_url = track['preview_url']
            print('cover art: ' + track['album']['images'][0]['url'])
            print()
        try:
            response = requests.get(preview_url)
            with open("preview.mp3", "wb") as file:
                file.write(response.content)
        except Exception as e:
            print(f"Connection error fetching preview: {e}")
    def playCurrentTracks(self):
        #Play user's saved tracks
        sp = self.sp
        try:
            results = sp.current_user_saved_tracks(limit=20)  #Get saved tracks
            
            #Check for an active Spotify device
            devices = sp.devices()
            if not devices['devices']:
                print("No active devices found. Open Spotify to play music.")
            else:
                device_id = devices['devices'][0]['id']  #Use first device

                while results:
                    track_uris = [item['track']['uri'] for item in results['items']] #Lookup songs from saved list
                    
                    #Start playing the tracks
                    sp.start_playback(device_id=device_id, uris=track_uris)
                    print("Playing saved songs...")
                    
                    #Check for more tracks (20 per page)
                    if results['next']:
                        results = sp.next(results)
                    else:
                        break
        except Exception as e:
            print(f"Cannot fetch or play user's songs: {e}")
client = SpotipyClient()
client.connectToSpotipy()
# client.playCurrentTracks()
client.loadSampleSong()
