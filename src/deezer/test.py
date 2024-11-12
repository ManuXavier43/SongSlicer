from spleeter.separator import Separator
import os

def split_vocals_instrumentals():
    # Define the input and output directories
    music_in_dir = "./music_in"
    music_out_dir = "./music_out"
    songs = [f for f in os.listdir(music_in_dir) if os.path.isfile(os.path.join(music_in_dir, f))]
    
    if not songs:
        print("No songs found in the music_in directory.")
        return
       
    print("Available songs:")
    for i, song in enumerate(songs, 1): # Display available songs to the user
        print(f"{i}. {song}")
    
    try:
        choice = int(input("Enter the number of the song you want to process: ")) - 1# Ask the user to select a song by its number
        if choice < 0 or choice >= len(songs):
            print("not a song please enter a number shown.")
            return
        
    except ValueError:
        print("Invalid. Please enter a number shown.")
        return

    
    input_file_path = os.path.join(music_in_dir, songs[choice])# Get the selected song's path
    song_name = os.path.splitext(songs[choice])[0]
    output_dir = os.path.join(music_out_dir, song_name)    # Create the output directory for the song in music_out
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize Spleeter with the 2-stem model (vocals and accompaniment)
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(input_file_path, output_dir)# splits the song into vocals and accompaniment
    print(f"Processing complete. Results saved in: {output_dir}")

# Run the splitting function within the main guard
if __name__ == '__main__':
    split_vocals_instrumentals()
