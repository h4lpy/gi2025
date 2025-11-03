from flask import Flask, jsonify, render_template, url_for
from config import FLAG
import qrcode
import random
import io
import base64
import secrets

app = Flask(__name__)

def generate_qr_code(data):
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate():
    qr_data_list = []
    count = 20  # Number of QR codes per batch
    include_flag = random.random() < 0.9999999

    if include_flag:
        flag_index = random.randint(0, count-1)
    else:
        flag_index = -1  # No flag

    for i in range(count):
        if i == flag_index:
            data = FLAG
        else:
            data = secrets.token_hex(22)
        qr_data_list.append(generate_qr_code(data))

    return jsonify(qrcodes=qr_data_list)

if __name__ == '__main__':
    app.run(debug=True)

