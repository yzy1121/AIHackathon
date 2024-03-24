import json
import base64
import wave

def convert_audio(data):
    # Get the audio data from the JSON
    audio_data = data['content']
    # Get the audio name from the JSON
    audio_name = data['date']

    params = data['params']
    # Decode the base64 encoded audio data
    decoded_audio = base64.b64decode(audio_data)

    # Write the decoded audio data to a .wav file, use the audio date as the file name
    with wave.open(f'{audio_name}.wav', 'wb') as wav_file:
        wav_file.setparams(tuple(params.values()))  # Set the original audio parameters
        wav_file.writeframes(decoded_audio)

    return f"{audio_name}.wav"

# Test the function with a sample JSON object
json_file = 'encoded_wav1.json'
with open(json_file, 'r') as file:
    data = json.load(file)
    convert_audio(data)