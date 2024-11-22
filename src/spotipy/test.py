import time
import spotipy, os #os for client secrets
import requests #Needed for fetching previews of songs
from dotenv import load_dotenv#Load environment variables

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth #Needed to connect to account
#Setup console logs
import logging
logging.basicConfig(level=logging.DEBUG)

#Spotipy Connector class
class SpotipyClient:
    def __init__(self, base_dir):
        self.sp = None
        self.base_dir = base_dir
    def connectToSpotipy(self):
        logging.debug("Connecting to Spotify API...") 
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
    def loadSampleSong(self,query):
        # query = input("Enter an artist to search: ")
        search_result = self.sp.search(q={query}, limit=1)
        #Search an artist and cycle through their previews
        artist_uri = search_result['tracks']['items'][0]['artists'][0]['uri']
        tracks = self.sp.artist_top_tracks(artist_uri, country='US')
        preview_url = tracks['tracks'][0]['preview_url']
        track_name = tracks['tracks'][0]['name']
        track_img = tracks['tracks'][0]['album']['images'][0]['url']
        # for track in tracks['tracks'][:5]:
        #     print('track    : ' + track['name'])
        #     print('audio    : ' + track['preview_url'])
        #     preview_url = track['preview_url']
        #     print('cover art: ' + track['album']['images'][0]['url'])
        #     print()
        try:
            #Find directory to save music
            music_dir = os.path.join(self.base_dir, "deezer/music_in")
            #ensure it exists
            os.makedirs(music_dir, exist_ok=True)
            response = requests.get(preview_url)
            #unique timestamp per song
            preview_filename = f"preview_{query.replace(' ', '_')}_{int(time.time())}.mp3"
            #actual path for preview
            preview_path = os.path.join(music_dir, preview_filename)
            logging.debug(f"Absolute path to saved file: {os.path.abspath(preview_path)}")
            #save to dir
            with open(preview_path, "wb") as file:
                file.write(response.content)
                logging.debug(f"Preview saved to {preview_path}")
                #only return filename as html knows the static folder
                return preview_filename,track_name,track_img
        except Exception as e:
            logging.debug(f"Connection error fetching preview: {e}")
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
# client = SpotipyClient()
# client.connectToSpotipy()
# # client.playCurrentTracks()
# client.loadSampleSong()
