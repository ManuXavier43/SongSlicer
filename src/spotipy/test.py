import spotipy
from spotipy.oauth2 import SpotifyOAuth #Needed to connect to account
#Spotipy Connector class
class SpotipyClient:
    def __init__(self):
        self.sp = None
    def connectToSpotipy(self):
        #Connect to Spotify API
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id="ca83c4a9c3234d01b9a97a5c7c89ab3a",
                client_secret="25e2b50606ab417fb0526c44a0437973",
                redirect_uri="http://localhost:8888/callback",
                scope="user-library-read user-modify-playback-state user-read-playback-state"
            ))
            print("Connected!")
        except Exception as e:
            print(f"Cannot connect to Spotify API: {e}")

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
client.playCurrentTracks()
