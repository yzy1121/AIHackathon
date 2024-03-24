import json
import base64
import subprocess
import os
import logging

# Configure logging to include the timestamp
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def convert_json_to_m4a(json_data):
    # Initialize temp_audio_path to None
    temp_audio_path = None

    try:
        # Decode the base64 audio content
        audio_data = base64.b64decode(json_data['content'])

        # Generate a unique file name using the date
        temp_audio_path = f"temp_{json_data['date']}.wav"  # Temporary file
        m4a_file_path = f"{json_data['date']}.m4a"  # Output file
        
        logging.info(f"Writing to temporary file: {temp_audio_path}")
        # Write the decoded audio data to the temporary file
        with open(temp_audio_path, 'wb') as temp_audio_file:
            temp_audio_file.write(audio_data)

        logging.info(f"Converting {temp_audio_path} to {m4a_file_path} using FFmpeg")
        # Convert the temporary audio file to M4A using ffmpeg
        result = subprocess.run(['ffmpeg', '-y', '-i', temp_audio_path, m4a_file_path],
                        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        
        logging.info(f"FFmpeg output: {result.stdout.decode()}")
        logging.info(f"Converted to M4A: {m4a_file_path}")

        # Return the path to the converted M4A file
        return m4a_file_path

    except KeyError as e:
        logging.error(f"Missing key in JSON data: {e}")
        return None  # Return None to indicate failure
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg error: {e.stderr.decode()}")
        return None  # Return None to indicate failure
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None  # Return None to indicate failure
    finally:
        # Cleanup: Remove the temporary WAV file if it exists and is defined
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            logging.info(f"Temporary file {temp_audio_path} has been deleted")

# Example usage
json_file_path = 'test1.json'  # Adjust the file path as needed

# Load JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)  # This should be a dictionary now

m4a_file_path = convert_json_to_m4a(json_data)

if m4a_file_path:
    logging.info(f"Conversion successful, M4A file saved at: {m4a_file_path}")
else:
    logging.error("Conversion failed.")
