import base64
import json
import time
import os

def encode_m4a_to_json(m4a_file_path):
    # Extract the base filename without the extension
    base_filename = os.path.splitext(m4a_file_path)[0]
    
    # Read the M4A file's binary content
    with open(m4a_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # Encode the binary data to base64
    encoded_audio = base64.b64encode(audio_data).decode('utf-8')

    # Construct a JSON object with the encoded data
    json_data = json.dumps({
        "content": encoded_audio,
        "date": time.strftime("%Y%m%d-%H%M%S"),
        "format": "m4a"
    })

    # Here, return both json_data and the base_filename
    return json_data, base_filename  # Return both values

# Example usage
m4a_file_path = 'test1.m4a'  # Replace with the path to your M4A file
json_data, base_filename = encode_m4a_to_json(m4a_file_path)  # This now correctly receives two values

# Save the JSON data to a file that shares the same base filename
json_file_path = f'{base_filename}.json'
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

print(f'JSON data has been saved to {json_file_path}')
