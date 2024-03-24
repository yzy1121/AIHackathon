# import base64
# import json
# import time

# def encode_wav_to_json(wav_file_path):
#     # Read the .wav file's binary content
#     with open(wav_file_path, 'rb') as wav_file:
#         wav_data = wav_file.read()

#     # Encode the binary data to base64
#     encoded_wav = base64.b64encode(wav_data).decode('utf-8')

#     # Construct a JSON object with the encoded data
#     json_data = json.dumps({"content": encoded_wav, "date": time.strftime("%Y%m%d-%H%M%S")})

#     return json_data

# wav_file_path = 'test1.wav'  # Replace with the path to your .wav file
# json_data = encode_wav_to_json(wav_file_path)

# # Now `json_data` contains your .wav file encoded as base64 in a JSON object
# # You can save this JSON data to a file or use it as needed
# # save the json data to a file
# with open('encoded_wav1.json', 'w') as json_file:
#     json_file.write(json_data)

import json
import base64
import wave
import time

def encode_wav_to_json(wav_file_path):
    # Open the WAV file and read properties
    try:
        with wave.open(wav_file_path, 'rb') as wav_file:
            n_channels = wav_file.getnchannels()
            sampwidth = wav_file.getsampwidth()
            framerate = wav_file.getframerate()
            wav_data = wav_file.readframes(wav_file.getnframes())

            # Encode the binary data to base64
            encoded_wav = base64.b64encode(wav_data).decode('utf-8')

            # Construct a JSON object with the encoded data and audio properties
            json_data = json.dumps({
                "content": encoded_wav,
                "date": time.strftime("%Y%m%d-%H%M%S"),
                "n_channels": n_channels,
                "sampwidth": sampwidth,
                "framerate": framerate
            })
            return json_data
    except wave.Error as e:
        print(f"Error processing {wav_file_path}: {e}")
        return None

wav_file_path = 'test1.wav'
json_data = encode_wav_to_json(wav_file_path)
if json_data is not None:
    # Save the JSON data to a file
    with open('encoded_wav1.json', 'w') as json_file:
        json_file.write(json_data)
else:
    print("No valid JSON data to write.")
