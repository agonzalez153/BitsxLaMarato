from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

# Contenido HTML simplificado y funcional
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Generador de Códigos QR</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            min-height: 100px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 8px 15px;
            margin: 5px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
        }
        .format-button {
            background-color: #2196F3;
        }
        #qrResult {
            margin-top: 20px;
            text-align: center;
        }
        #qrResult img {
            max-width: 300px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Generador de Códigos QR</h1>

        <div>
            <button type="button" class="format-button" onclick="insertFormat('**', '**')">Negrita</button>
            <button type="button" class="format-button" onclick="insertFormat('_', '_')">Cursiva</button>
        </div>

        <textarea id="textInput" placeholder="Escribe tu texto aquí..."></textarea>

        <button onclick="generateQR()">Generar QR</button>

        <div id="qrResult"></div>
    </div>

    <script>
        function insertFormat(startTag, endTag) {
            const textarea = document.getElementById('textInput');
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const text = textarea.value;

            const selectedText = text.substring(start, end);
            const replacement = startTag + selectedText + endTag;

            textarea.value = text.substring(0, start) + replacement + text.substring(end);

            // Mantener el foco en el textarea
            textarea.focus();
            textarea.setSelectionRange(start + startTag.length, end + startTag.length);
        }

        function generateQR() {
            const text = document.getElementById('textInput').value;
            if (!text) {
                alert('Por favor, ingresa algún texto');
                return;
            }

            // Procesar el texto para aplicar el formato
            let processedText = text
                .replace(/\*\*(.*?)\*\*/g, '$1')  // Procesar negrita
                .replace(/_(.*?)_/g, '$1');       // Procesar cursiva

            fetch('/generate_qr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'text=' + encodeURIComponent(processedText)
            })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const img = document.createElement('img');
                img.src = url;
                const resultDiv = document.getElementById('qrResult');
                resultDiv.innerHTML = '';
                resultDiv.appendChild(img);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al generar el código QR');
            });
        }
    </script>
</body>
</html>
"""

# Asegúrate de que existe el directorio templates
import os

if not os.path.exists('templates'):
    os.makedirs('templates')

# Guardar el contenido HTML en un archivo
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    try:
        text = request.form.get('text', '')

        # Configuración del código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Agregar datos y generar el código QR
        qr.add_data(text)
        qr.make(fit=True)

        # Crear la imagen
        img = qr.make_image(fill_color="black", back_color="white")

        # Guardar la imagen en un buffer
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        return send_file(img_buffer, mimetype='image/png')

    except Exception as e:
        print(f"Error: {str(e)}")
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)