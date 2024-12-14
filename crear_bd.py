import sqlite3

# Crear conexión a la base de datos SQLite
conn = sqlite3.connect("enfermedades_pulmonares.db")
cursor = conn.cursor()

# Crear tablas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Diagnostico (
    ID_Diagnostico INTEGER PRIMARY KEY,
    Tipo_MPDI TEXT,
    Causa_Agudizacion TEXT,
    Tratamiento_Base TEXT,
    Immunosupresion TEXT,
    Comorbilidades TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Diagnostico_Concreto (
    ID_DiagnosticoConcreto INTEGER PRIMARY KEY,
    Diagnostico TEXT,
    Tratamiento_Especifico TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Tratamiento_General (
    ID_Tratamiento INTEGER PRIMARY KEY,
    Medicamento TEXT,
    Dosis TEXT,
    Frecuencia TEXT,
    Observaciones TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Causas_Agudizacion (
    ID_Causa INTEGER PRIMARY KEY,
    Causa TEXT,
    Detalles TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Procedimientos (
    ID_Procedimiento INTEGER PRIMARY KEY,
    Procedimiento TEXT,
    Detalles TEXT
)
''')

# Insertar datos de ejemplo
cursor.execute('''
INSERT INTO Diagnostico (ID_Diagnostico, Tipo_MPDI, Causa_Agudizacion, Tratamiento_Base, Immunosupresion, Comorbilidades)
VALUES (1, 'FPI', 'Tromboembolismo pulmonar', 'Losartan', 'Sí', 'Insuficiencia cardíaca')
''')

cursor.execute('''
INSERT INTO Diagnostico_Concreto (ID_DiagnosticoConcreto, Diagnostico, Tratamiento_Especifico)
VALUES (1, 'Neumonía', 'Cefalosporina 3ªG + Levofloxacino')
''')

cursor.execute('''
INSERT INTO Tratamiento_General (ID_Tratamiento, Medicamento, Dosis, Frecuencia, Observaciones)
VALUES (1, 'Omeprazol', '20 mg', 'Cada 12-24h', 'Inhibidor bomba de protones')
''')

cursor.execute('''
INSERT INTO Tratamiento_General (ID_Tratamiento, Medicamento, Dosis, Frecuencia, Observaciones)
VALUES (2, 'Morfina', '2.5-5 mg', 'Puntual', 'Para disnea intensa')
''')

cursor.execute('''
INSERT INTO Causas_Agudizacion (ID_Causa, Causa, Detalles)
VALUES (1, 'Infecciones', 'Virus, hongos, bacterias')
''')

cursor.execute('''
INSERT INTO Causas_Agudizacion (ID_Causa, Causa, Detalles)
VALUES (2, 'Tromboembolismo pulmonar', 'Incluye embólia grasa')
''')

cursor.execute('''
INSERT INTO Procedimientos (ID_Procedimiento, Procedimiento, Detalles)
VALUES (1, 'Angio-TACAR', 'Detección de TEP')
''')

cursor.execute('''
INSERT INTO Procedimientos (ID_Procedimiento, Procedimiento, Detalles)
VALUES (2, 'Gasometría arterial', 'Valoración de PaO2/FIO2')
''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada y datos insertados con éxito.")
