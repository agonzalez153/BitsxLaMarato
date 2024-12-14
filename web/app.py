from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
do_PCR = False
PCR = False
immunosuprimit = False
tmespecific = False
fumador = False
hipertensio_pulmonar = False
sospites_epital = False
hipoTA = False

tinza = False
cmv = False
pnj = False

TRACTAMENTS = {
    'oxigenoterapia': 'OXIGENOTERAPIA Ajustar FiO2 según requerimientos (SatO2 > 92%)',
    'oseltamivir': 'Oseltamivir 75mg/12h v.o.',
    'cefalosporina': 'Cefalosporina 3ªG',
    'levofloxacino': 'Levofloxacino 500 mg/24h v.o.',
    'inhibidor_bomba_protons': 'Omeprazol 20 mg/12-24h e.v.',
    'piperacilina': 'Piperacilina/Tazobactam 4g/0,5g/8h e.v. (ó cefalosporina 3ª generació)',
    'ganciclovir': 'Ganciclovir 5mg/Kg pes/12h e.v.',
    'sulfametoxazol': 'Sulfametoxazol/Trimetoprim 800/160mg/12h e.v.',
    'ac_folic': 'Ac.Folic',
    'oxigenoterapia': 'OXIGENOTERAPIA ajustant FIO2 segons requeriments (SatO2 > 92%)',
    'acetilcisteina': 'N-ACETILCISTEÏNA 600 mg/8h v.o. (potent antioxidant pulmonar)',
    'nebulitacions': 'Nebulitzacions amb 1,5-2cc atrovent + 2cc SF +/- 0,5cc salbutamol',
    'morfina': 'MORFINA 2,5-5mg s.c. puntual si dispnea intensa',
    'hbpm_bemi': 'HBPM: Bemiparina 2500-3500 UI/0,2 mL (segons Kg pes) s.c./dia',
    'hbpm_tinza': ' HBPM (Tinzaparina 20000UI 0,5-0,9 mL (segons Kg pes)) s.c./dia',
    'metilprednis': 'METILPREDNISOLONA (en casos específics): ½-1 mg/Kg pes/d e.v   +  CALCI +Vit D 500mg/400 UI: 2comp/d v.o.',
    'losartan': 'LOSARTAN 50mg/24h v.o. (antiapoptòtic epitelial)',
    'ttmespecific': 'Ttm específic',
}

tractaments_client = []


@app.route('/')
def inici():
    return render_template('inici.html')


@app.route('/radiografia-torax', methods=['GET', 'POST'])
def radiografia_torax():
    if request.method == 'POST':
        tiene_infiltrados = request.form.get('tiene_infiltrados') == 'true'
        if tiene_infiltrados:
            return redirect(url_for('sospites_grip_covid'))
        return redirect(url_for('final_felic'))
    return render_template('radiografia-torax.html')

@app.route('/final-felic')
def final_felic():
    return render_template('final-felic.html')

@app.route('/sospites-grip-covid', methods=['GET', 'POST'])
def sospites_grip_covid():
    do_PCR = False
    if request.method == 'POST':
        sospites_grip = request.form.get('sospites_grip') == 'true'
        sospites_covid = request.form.get('sospites_covid') == 'true'
        do_PCR = sospites_grip or sospites_covid
        if do_PCR:
            return redirect(url_for('micro_anti_hemo_pcr'))
        return redirect(url_for('micro_anti_hemo'))
    return render_template('sospites-grip-covid.html')

@app.route('/micro-anti-hemo')
def micro_anti_hemo():
    return render_template('micro-anti-hemo.html')

@app.route('/micro-anti-hemo-pcr')
def micro_anti_hemo_pcr():
    return render_template('micro-anti-hemo-pcr.html')

@app.route('/dx-pn', methods=['GET', 'POST'])
def dx_pn():
    PCR, tmespecific = False, False
    if request.method == 'POST':
        dx_concret = request.form.get('diagnostic_concretat') == 'true'
        pneumonia = request.form.get('pneumonia') == 'true'
        PCR = request.form.get('pcr_positiva') == 'true'
        if dx_concret:
            if pneumonia:
                if immunosuprimit:
                    return redirect(url_for('sospites_cmv_pnj'))
                return redirect(url_for('tractament'))
            tmespecific = True
            return redirect(url_for('tractament'))
        return redirect(url_for('sospites_tec'))
    if do_PCR:
        return render_template('dx-pn_goc.html')
    return render_template('dx-pn.html')

@app.route('/dx-pn_goc', methods=['GET', 'POST'])
def dx_pn_goc():
    PCR, tmespecific = False, False
    if request.method == 'POST':
        dx_concret = request.form.get('diagnostic_concretat') == 'true'
        pneumonia = request.form.get('pneumonia') == 'true'
        PCR = request.form.get('pcr_positiva') == 'true'
        if dx_concret:
            if pneumonia:
                if immunosuprimit:
                    return redirect(url_for('sospites_cmv_pnj'))
                return redirect(url_for('tractament'))
            tmespecific = True
            return redirect(url_for('tractament'))
        return redirect(url_for('sospites_tec'))
    return render_template('dx-pn_goc.html')

@app.route('/sospites-cmv-pnj', methods=['GET', 'POST'])
def sospites_cmv_pnj():
    cmv, pnj = False, False
    if request.method == 'POST':
        sospites_cmv = request.form.get('sospites_cmv') == 'true'
        sospites_pnj = request.form.get('sospites_pnj') == 'true'
        if sospites_cmv:
            cmv = True
        if sospites_pnj:
            pnj = True
        return redirect(url_for('tractament'))
    return render_template('sospites-cmv-pnj.html')

@app.route('/sospites-tec', methods=['GET', 'POST'])
def sospites_tec():
    tinza, val_parenq = False, False
    if request.method == 'POST':
        sospites_TEC = request.form.get('sospites_tec') == 'true'
        if sospites_TEC:
            return redirect(url_for('angio_ddimer'))
        return redirect(url_for('val_parenq'))
    return render_template('sospites-tec.html')

@app.route('/angio-ddimer')
def angio_ddimer():
    tinza = True
    return render_template('angio-ddimer.html')

@app.route('/val-parenq')
def val_parenq():
    tmespecific = True
    return render_template('val-parenq.html')

@app.route('/tractament')
def tractament():
    tractaments_client = []
    if not immunosuprimit:
        tractaments_client.extend(['oseltamivir', 'cefalosporina', 'levofloxacino'])
    else:
        tractaments_client.extend(['piperacilina', 'levofloxacino'])
        if tinza:
            tractaments_client.extend(['hbpm_tinza'])
        if cmv:
            tractaments_client.extend(['ganciclovir'])
    if pnj:
        tractaments_client.extend(['sulfametoxazol','ac_folic'])
    tractaments_client.extend(['oxigenoterapia','inhibidor_bomba_protons','acetilcisteina','morfina','hbpm_bemi','metilprednis'])
    if fumador and not hipertensio_pulmonar:
        tractaments_client.append(['nebulitacions'])
    if sospites_epital and not hipoTA:
        tractaments_client.append(['losartan'])
    return render_template('tractament.html', tractaments_client=tractaments_client, TRACTAMENTS=TRACTAMENTS)

if __name__ == '__main__':
    app.run(debug=True)
