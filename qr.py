from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import os

# Inicializar la aplicación Flask
app = Flask(__name__)

# Asegurarse de que existe el directorio para las plantillas
if not os.path.exists('templates'):
    os.makedirs('templates')

# Crear el archivo HTML si no existe
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Códigos QR</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f2f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1a73e8;
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #1a73e8;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #1557b0;
        }
        #qrResult {
            text-align: center;
            margin-top: 20px;
        }
        img {
            max-width: 300px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Generador de Códigos QR</h1>
        <div class="form-group">
            <input type="text" id="text" placeholder="Ingrese el texto para el código QR">
        </div>
        <button onclick="generateQR()">Generar QR</button>
        <div id="qrResult"></div>
    </div>

    <script>
        function generateQR() {
            const text = document.getElementById('text').value;
            if (text) {
                fetch('/generate_qr', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `text=${encodeURIComponent(text)}`
                })
                .then(response => response.blob())
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const img = document.createElement('img');
                    img.src = url;
                    const resultDiv = document.getElementById('qrResult');
                    resultDiv.innerHTML = '';
                    resultDiv.appendChild(img);
                });
            }
        }
    </script>
</body>
</html>
"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)


# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')


# Ruta para generar el código QR
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    # Obtener el texto del formulario
    text = request.form.get('text', '')

    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Crear la imagen del código QR
    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen en un buffer
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
