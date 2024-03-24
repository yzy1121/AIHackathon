# import json
# import base64
# import wave

# def convert_audio(data):
#     # Get the audio data from the JSON
#     audio_data = data['content']
#     # Get the audio name from the JSON
#     audio_name = data['date']
#     # Decode the base64 encoded audio data
#     decoded_audio = base64.b64decode(audio_data)

#     # Write the decoded audio data to a .wav file, use the audio date as the file name
#     with wave.open(f'{audio_name}.wav', 'wb') as wav_file:
#         wav_file.setnchannels(1)  # Set the number of channels (1 for mono, 2 for stereo)
#         wav_file.setsampwidth(2)  # Set the sample width (2 bytes for 16-bit audio)
#         wav_file.setframerate(44100)  # Set the sample rate (44100 Hz is standard for audio)
#         wav_file.writeframes(decoded_audio)

# file_name = 'encoded_wav1.json'
# with open(file_name, 'r') as file:
#     data = json.load(file)

# convert_audio(data)

import json
import base64
import wave

def convert_json_to_audio(json_file_path):
    # Load the JSON data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    audio_data = base64.b64decode(data['content'])
    audio_name = data['date']

    # Use the properties from the JSON
    with wave.open(f'{audio_name}.wav', 'wb') as wav_file:
        wav_file.setnchannels(data['n_channels'])
        wav_file.setsampwidth(data['sampwidth'])
        wav_file.setframerate(data['framerate'])
        wav_file.writeframes(audio_data)

# Example usage
json_file_path = 'encoded_wav1.json'
convert_json_to_audio(json_file_path)
