from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

TRATAMIENTOS = {
    'oxigenoterapia': 'Ajustar FiO2 según requerimientos (SatO2 > 92%).',
    'inhibidor_bomba_protons': 'Omeprazol 20 mg/12-24h e.v.',
    'piperacilina': 'Piperacilina/Tazobactam 4g/0,5g/8h e.v. (dosis de cefalosporina 3a + Levofloxacino 500mg/24h)',
    'ganciclovir': 'Ganciclovir 5mg/Kg pes/12h e.v.',
    'sulfametoxazol': 'Sulfametoxazol/Trimetoprim 800/160mg/12h e.v. + Ac.Folic'
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/radiografia-torax', methods=['GET', 'POST'])
def radiografia_torax():
    if request.method == 'POST':
        tiene_infiltrados = request.form.get('tiene_infiltrados') == 'true'
        return redirect(url_for('diagnostico', tiene_infiltrados=tiene_infiltrados))
    return render_template('radiografia-torax.html')


@app.route('/diagnostico')
def diagnostico():
    tiene_infiltrados = request.args.get('tiene_infiltrados', False, bool)
    if tiene_infiltrados:
        return redirect(url_for('pcr'))
    else:
        return redirect(url_for('tratamiento'))


@app.route('/pcr', methods=['GET', 'POST'])
def pcr():
    if request.method == 'POST':
        pcr_positiva = request.form.get('pcr_positiva') == 'true'
        inmunosupressio = request.form.get('inmunosupressio') == 'true'
        return redirect(url_for('tratamiento', pcr_positiva=pcr_positiva, inmunosupressio=inmunosupressio))
    return render_template('pcr.html')


@app.route('/tratamiento')
def tratamiento():
    pcr_positiva = request.args.get('pcr_positiva', False, bool)
    inmunosupressio = request.args.get('inmunosupressio', False, bool)

    tratamiento = []
    if pcr_positiva:
        if inmunosupressio:
            tratamiento.extend(['piperacilina', 'ganciclovir', 'sulfametoxazol'])
        else:
            tratamiento.extend(['oseltamivir', 'cefalosprina', 'levofloxacino'])
    else:
        tratamiento.extend(['oxigenoterapia', 'inhibidor_bomba_protons'])

    return render_template('tratamiento.html', tratamiento=tratamiento, TRATAMIENTOS=TRATAMIENTOS)

if __name__ == '__main__':
    app.run(debug=True)