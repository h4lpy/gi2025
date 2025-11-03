import sys
import requests
import base64
import io
from PIL import Image
from pyzbar.pyzbar import decode

FLAG_PREFIX = 'flag{'
BATCH_SIZE = 20
url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000/generate'

qr_counter = 0  # Total number of QR codes scanned

def decode_qr_from_base64(b64_data):
    image_data = base64.b64decode(b64_data)
    img = Image.open(io.BytesIO(image_data))
    decoded = decode(img)
    return decoded[0].data.decode() if decoded else None

while True:
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Failed to get QR codes. Status code: {response.status_code}')
        break

    qr_images = response.json().get('qrcodes', [])
    for b64 in qr_images:
        qr_counter += 1
        data = decode_qr_from_base64(b64)
        if data and FLAG_PREFIX in data:
            print(f'[✓] Flag found: {data}')
            print(f'[✓] Found at QR number #{qr_counter}')
            exit(0)

    print(f'Checked {qr_counter} QR codes so far... flag not found yet.')
