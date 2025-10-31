from flask import Flask, jsonify, render_template, url_for
import qrcode
import random
import io
import base64

app = Flask(__name__)
FLAG = 'flag{h1dd3n_am0ngs7_s0me_qr_c0d3s}'

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
    include_flag = random.random() < 0.005

    if include_flag:
        flag_index = random.randint(0, count-1)
    else:
        flag_index = -1  # No flag

    for i in range(count):
        if i == flag_index:
            data = FLAG
        else:
            data = f'junk_{random.randint(100000, 999999)}'
        qr_data_list.append(generate_qr_code(data))

    return jsonify(qrcodes=qr_data_list)

if __name__ == '__main__':
    app.run(debug=True)
