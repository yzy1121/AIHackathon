import json
import base64
import subprocess
import os

def convert_json_to_m4a(json_file_path):
    try:
        # Load the JSON data
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Decode the base64 audio content
        audio_data = base64.b64decode(data['content'])

        # Temporary file for the decoded audio
        temp_audio_path = f"{data['date']}.tmp"
        # Target M4A file path
        m4a_file_path = f"{data['date']}.m4a"
        
        # Write the decoded audio data to a temporary file
        with open(temp_audio_path, 'wb') as temp_audio_file:
            temp_audio_file.write(audio_data)

        # Convert the temporary audio file to M4A using ffmpeg
        subprocess.run(['ffmpeg', '-i', temp_audio_path, m4a_file_path])
        print(f"Converted to M4A: {m4a_file_path}")

    except KeyError as e:
        print(f"Missing key in JSON data: {e}")
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup: Remove the temporary file if it exists
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

# Example usage
json_file_path = 'test1.json'  # Adjust the file path as needed
convert_json_to_m4a(json_file_path)
