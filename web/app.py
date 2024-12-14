from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# Diccionario de síntomas y enfermedades
SINTOMAS_ENFERMEDADES = {
    'gripe': ['fiebre', 'tos', 'dolor_muscular', 'fatiga'],
    'covid': ['fiebre', 'tos_seca', 'cansancio', 'perdida_olfato'],
    'resfriado': ['estornudos', 'congestion_nasal', 'dolor_garganta'],
    'diabetes': ['sed_excesiva', 'orinar_frecuentemente', 'perdida_peso'],
    'hipertension': ['dolor_cabeza', 'mareos', 'vision_borrosa']
}


@app.route('/')
def index():
    return render_template('index.html', sintomas=list(set([s for enf in SINTOMAS_ENFERMEDADES.values() for s in enf])))


@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    sintomas_seleccionados = request.json.get('sintomas', [])

    # Lógica de diagnóstico simple
    posibles_enfermedades = []
    for enfermedad, sintomas_enfermedad in SINTOMAS_ENFERMEDADES.items():
        coincidencias = len(set(sintomas_seleccionados) & set(sintomas_enfermedad))
        if coincidencias > 0:
            posibles_enfermedades.append({
                'nombre': enfermedad,
                'coincidencias': coincidencias
            })

    posibles_enfermedades.sort(key=lambda x: x['coincidencias'], reverse=True)

    return jsonify(posibles_enfermedades)


if __name__ == '__main__':
    app.run(debug=True)