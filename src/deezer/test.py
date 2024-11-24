import re
import os
import shutil
from spleeter.separator import Separator

def split_vocals_instrumentals(music_in_dir, music_out_dir, song_name):
    # Sanitize the song name to avoid issues with special characters
    sanitized_song_name = re.sub(r'[^a-zA-Z0-9]', '_', os.path.splitext(song_name)[0])

    # Get the selected song's path
    input_file_path = os.path.join(music_in_dir, song_name)
    # Save the output initially in a temp directory inside music_out
    temp_output_dir = os.path.join(music_out_dir, sanitized_song_name, "temp")

    # Create the output directory for the song in music_out
    os.makedirs(temp_output_dir, exist_ok=True)

    # Initialize Spleeter with the 2-stem model (vocals and accompaniment)
    separator = Separator('spleeter:2stems')

    try:
        # Split the input file into vocals and accompaniment using Spleeter
        separator.separate_to_file(input_file_path, temp_output_dir)

        # After splitting, move the generated files to flatten the structure
        final_output_dir = os.path.join(music_out_dir, sanitized_song_name)
        os.makedirs(final_output_dir, exist_ok=True)

        # Move files from the temp folder to the final output folder
        for root, _, files in os.walk(temp_output_dir):
            for file in files:
                shutil.move(os.path.join(root, file), os.path.join(final_output_dir, file))

        # Remove the temp folder after files are moved
        shutil.rmtree(temp_output_dir)

        print(f"Processing complete. Results saved in: {final_output_dir}")

    except Exception as e:
        print(f"An error occurred while processing the song: {e}")
