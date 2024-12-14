from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import os

app = Flask(__name__)

# Contenido HTML actualizado con textarea en lugar de input
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Códigos QR - Texto Multilínea</title>
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
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            min-height: 150px;
            resize: vertical;
            font-family: Arial, sans-serif;
        }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        button {
            background-color: #1a73e8;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            flex: 1;
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
        .format-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        .format-button {
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            color: #333;
            padding: 5px 10px;
            cursor: pointer;
        }
        .format-button:hover {
            background-color: #e9ecef;
        }
        #previewText {
            margin-top: 10px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
            white-space: pre-wrap;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Generador de Códigos QR</h1>
        <div class="format-buttons">
            <button class="format-button" onclick="insertFormat('**texto**')">Negrita</button>
            <button class="format-button" onclick="insertFormat('_texto_')">Cursiva</button>
            <button class="format-button" onclick="insertFormat('* ')">Lista</button>
        </div>
        <div class="form-group">
            <textarea id="text" placeholder="Ingrese el texto para el código QR (puede usar múltiples líneas)"></textarea>
        </div>
        <div class="controls">
            <button onclick="generateQR()">Generar QR</button>
            <button onclick="previewText()" style="background-color: #34a853;">Vista Previa</button>
        </div>
        <div id="previewText"></div>
        <div id="qrResult"></div>
    </div>

    <script>
        function insertFormat(format) {
            const textarea = document.getElementById('text');
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const text = textarea.value;

            const beforeText = text.substring(0, start);
            const selectedText = text.substring(start, end);
            const afterText = text.substring(end);

            if (format === '* ') {
                // Para listas, insertar al inicio de la línea
                textarea.value = beforeText + format + selectedText + afterText;
            } else {
                // Para otros formatos, envolver el texto seleccionado
                const formattedText = format.replace('texto', selectedText || 'texto');
                textarea.value = beforeText + formattedText + afterText;
            }
        }

        function previewText() {
            const text = document.getElementById('text').value;
            const previewDiv = document.getElementById('previewText');

            // Convertir el texto plano a HTML
            let htmlText = text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/_(.*?)_/g, '<em>$1</em>')
                .replace(/^\* (.*)$/gm, '•&nbsp;$1')
                .replace(/\n/g, '<br>');

            previewDiv.innerHTML = htmlText;
            previewDiv.style.display = htmlText ? 'block' : 'none';
        }

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    text = request.form.get('text', '')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)