import base64
import json
import time

def encode_wav_to_json(wav_file_path):
    # Read the .wav file's binary content
    with open(wav_file_path, 'rb') as wav_file:
        wav_data = wav_file.read()

    # Encode the binary data to base64
    encoded_wav = base64.b64encode(wav_data).decode('utf-8')

    # Construct a JSON object with the encoded data
    json_data = json.dumps({"content": encoded_wav, "date": time.strftime("%Y%m%d-%H%M%S")})

    return json_data

wav_file_path = 'test1.wav'  # Replace with the path to your .wav file
json_data = encode_wav_to_json(wav_file_path)

# Now `json_data` contains your .wav file encoded as base64 in a JSON object
# You can save this JSON data to a file or use it as needed
# save the json data to a file
with open('encoded_wav1.json', 'w') as json_file:
    json_file.write(json_data)

