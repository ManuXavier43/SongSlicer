import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Connect to Spotify API with playback permissions
sp = None
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
         client_id="##########",
        client_secret="KEY",
        redirect_uri="http://localhost:8888/callback",
        scope="user-library-read user-modify-playback-state user-read-playback-state"
    ))
    print("Connected!")
except Exception as e:
    print(f"Cannot connect to Spotify API: {e}")

# Fetch and play the user's saved tracks
try:
    results = sp.current_user_saved_tracks(limit=20)  # Get the first page of saved tracks
    
    # Check for an active Spotify device
    devices = sp.devices()
    if not devices['devices']:
        print("No active devices found. Make sure Spotify is open on a device.")
    else:
        device_id = devices['devices'][0]['id']  # Use the first available device

        while results:
            track_uris = [item['track']['uri'] for item in results['items']]
            
            # Start playing the tracks
            sp.start_playback(device_id=device_id, uris=track_uris)
            print("Playing saved songs...")
            
            # Check for more tracks (pagination)
            if results['next']:
                results = sp.next(results)
            else:
                break
except Exception as e:
    print(f"Cannot fetch or play user's songs: {e}")
