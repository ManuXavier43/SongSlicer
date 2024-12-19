import deezer 
# from dotenv import load_dotenv #previously needed for spotipy
#Setup console logs
import logging
logging.basicConfig(level=logging.DEBUG)

#Deezer Connector class
class DeezerClient:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.link = "https://api.deezer.com"
        self.cli = None
    def loadSampleSong(self, query):
        """
        Search for an artist on Deezer and fetch their top tracks.
        """
        try:
            self.cli = deezer.Client() #create client
            tracks = self.cli.search(query) #search song
            track_list = []
            for track in tracks[:3]:  # Limit to 3 tracks
                track_info = { #name, preview, image used in html
                    "name": track.title,
                    "preview_url": track.preview,
                    "album_image": track.album.cover_medium  # Medium-sized album cover
                }
                track_list.append(track_info)
            
            return track_list

        except Exception as e:
            logging.debug(f"Cannot fetch tracks: {e}")
            return None
    # def playCurrentTracks(self):
    #     #Play user's saved tracks
    #     sp = self.sp
    #     try:
    #         results = sp.current_user_saved_tracks(limit=20)  #Get saved tracks
            
    #         #Check for an active Spotify device
    #         devices = sp.devices()
    #         if not devices['devices']:
    #             print("No active devices found. Open Spotify to play music.")
    #         else:
    #             device_id = devices['devices'][0]['id']  #Use first device

    #             while results:
    #                 track_uris = [item['track']['uri'] for item in results['items']] #Lookup songs from saved list
                    
    #                 #Start playing the tracks
    #                 sp.start_playback(device_id=device_id, uris=track_uris)
    #                 print("Playing saved songs...")
                    
    #                 #Check for more tracks (20 per page)
    #                 if results['next']:
    #                     results = sp.next(results)
    #                 else:
    #                     break
    #     except Exception as e:
    #         print(f"Cannot fetch or play user's songs: {e}")
# client = SpotipyClient()
# client.connectToSpotipy()
# # client.playCurrentTracks()
# client.loadSampleSong()

'''OLD SPOTIPY CODE'''
    # def connectToSpotipy(self):
    #     logging.debug("Connecting to Spotify API...") 
    #     #Connect to Spotify API
    #     try:
    #         load_dotenv()
    #         self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    #             client_id=os.getenv("CLIENT_ID"),
    #             client_secret=os.getenv("SPOTIFY_SECRET"),
    #             redirect_uri="http://localhost:8888/callback",
    #             scope="user-library-read user-modify-playback-state user-read-playback-state"
    #         ))
    #         print("Connected!")
    #     except Exception as e:
    #         print(f"Cannot connect to Spotify API: {e}")
    #         return False
