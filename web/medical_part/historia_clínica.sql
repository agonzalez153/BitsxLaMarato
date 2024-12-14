-- Crear tabla Paciente
CREATE TABLE Paciente (
    ID_Paciente SERIAL PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Apellidos TEXT NOT NULL,
    Fecha_Nacimiento DATE,
    NHC TEXT UNIQUE NOT NULL,  -- Número Historia Clínica
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    qr_code TEXT UNIQUE,
    qr_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Modificar tabla Diagnostico para incluir relación con Paciente
CREATE TABLE Diagnostico (
    ID_Diagnostico SERIAL PRIMARY KEY,
    ID_Paciente INTEGER REFERENCES Paciente(ID_Paciente),
    Fecha_Diagnostico DATE DEFAULT CURRENT_DATE,
    Tipo_MPDI TEXT NOT NULL,
    Causa_Agudizacion TEXT NOT NULL,
    Tratamiento_Base TEXT,
    Immunosupresion TEXT,
    Comorbilidades TEXT,
    Activo BOOLEAN DEFAULT true
);

-- Crear la tabla Diagnostico_Concreto
CREATE TABLE Diagnostico_Concreto (
    ID_DiagnosticoConcreto SERIAL PRIMARY KEY,
    Diagnostico TEXT NOT NULL,
    Tratamiento_Especifico TEXT
);

-- Crear la tabla Tratamiento_General
CREATE TABLE Tratamiento_General (
    ID_Tratamiento SERIAL PRIMARY KEY,
    Medicamento TEXT NOT NULL,
    Dosis TEXT,
    Frecuencia TEXT,
    Observaciones TEXT
);

-- Crear la tabla Causas_Agudizacion
CREATE TABLE Causas_Agudizacion (
    ID_Causa SERIAL PRIMARY KEY,
    Causa TEXT NOT NULL,
    Detalles TEXT
);

-- Crear la tabla Procedimientos
CREATE TABLE Procedimientos (
    ID_Procedimiento SERIAL PRIMARY KEY,
    Procedimiento TEXT NOT NULL,
    Detalles TEXT
);

-- Crear tabla para gestión de QR
CREATE TABLE Paciente_QR (
    id_qr SERIAL PRIMARY KEY,
    id_paciente INTEGER REFERENCES Paciente(ID_Paciente),
    qr_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Insertar datos en la tabla Diagnostico
INSERT INTO Diagnostico (Tipo_MPDI, Causa_Agudizacion, Tratamiento_Base, Immunosupresion, Comorbilidades)
VALUES ('FPI', 'Tromboembolismo pulmonar', 'Losartan', 'Sí', 'Insuficiencia cardíaca');

-- Insertar datos en la tabla Diagnostico_Concreto
INSERT INTO Diagnostico_Concreto (Diagnostico, Tratamiento_Especifico)
VALUES ('Neumonía', 'Cefalosporina 3ªG + Levofloxacino');

-- Insertar datos en la tabla Tratamiento_General
INSERT INTO Tratamiento_General (Medicamento, Dosis, Frecuencia, Observaciones)
VALUES
('Omeprazol', '20 mg', 'Cada 12-24h', 'Inhibidor bomba de protones'),
('Morfina', '2.5-5 mg', 'Puntual', 'Para disnea intensa');

-- Insertar datos en la tabla Causas_Agudizacion
INSERT INTO Causas_Agudizacion (Causa, Detalles)
VALUES
('Infecciones', 'Virus, hongos, bacterias'),
('Tromboembolismo pulmonar', 'Incluye embólia grasa');

-- Insertar datos en la tabla Procedimientos
INSERT INTO Procedimientos (Procedimiento, Detalles)
VALUES
('Angio-TACAR', 'Detección de TEP'),
('Gasometría arterial', 'Valoración de PaO2/FIO2');

-- Crear vistas para la web
CREATE OR REPLACE VIEW vista_historia_clinica AS
SELECT 
    p.NHC,
    p.Nombre,
    p.Apellidos,
    p.qr_code,
    d.Tipo_MPDI,
    d.Causa_Agudizacion,
    dc.Diagnostico as Diagnostico_Actual,
    dc.Tratamiento_Especifico,
    tg.Medicamento,
    tg.Dosis,
    tg.Frecuencia
FROM Paciente p
JOIN Diagnostico d ON p.ID_Paciente = d.ID_Paciente
LEFT JOIN Diagnostico_Concreto dc ON d.ID_Diagnostico = dc.ID_DiagnosticoConcreto
LEFT JOIN Tratamiento_General tg ON d.ID_Diagnostico = tg.ID_Tratamiento
WHERE d.Activo = true;

-- Crear índices para mejorar rendimiento
CREATE INDEX idx_paciente_nhc ON Paciente(NHC);
CREATE INDEX idx_diagnostico_paciente ON Diagnostico(ID_Paciente);

-- Función para obtener historia clínica completa
CREATE OR REPLACE FUNCTION obtener_historia_clinica(p_nhc TEXT)
RETURNS TABLE (
    nombre_completo TEXT,
    diagnostico_actual TEXT,
    tratamientos JSON,
    procedimientos JSON
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.Nombre || ' ' || p.Apellidos,
        d.Tipo_MPDI,
        json_agg(DISTINCT jsonb_build_object(
            'medicamento', tg.Medicamento,
            'dosis', tg.Dosis,
            'frecuencia', tg.Frecuencia
        )) as tratamientos,
        json_agg(DISTINCT jsonb_build_object(
            'procedimiento', pr.Procedimiento,
            'detalles', pr.Detalles
        )) as procedimientos
    FROM Paciente p
    JOIN Diagnostico d ON p.ID_Paciente = d.ID_Paciente
    LEFT JOIN Tratamiento_General tg ON d.ID_Diagnostico = tg.ID_Tratamiento
    LEFT JOIN Procedimientos pr ON d.ID_Diagnostico = pr.ID_Procedimiento
    WHERE p.NHC = p_nhc
    GROUP BY p.Nombre, p.Apellidos, d.Tipo_MPDI;
END;
$$ LANGUAGE plpgsql;

-- Función para generar QR único
CREATE OR REPLACE FUNCTION generate_patient_qr(p_id_paciente INTEGER)
RETURNS TEXT AS $$
DECLARE
    qr_text TEXT;
BEGIN
    -- Generar QR único combinando ID, timestamp y un número aleatorio
    qr_text := 'PAT-' || p_id_paciente::TEXT || '-' ||
               extract(epoch from current_timestamp)::TEXT || '-' ||
               floor(random() * 1000)::TEXT;
    
    -- Insertar nuevo QR
    INSERT INTO Paciente_QR (id_paciente, qr_data)
    VALUES (p_id_paciente, qr_text);
    
    -- Actualizar QR en tabla Paciente
    UPDATE Paciente
    SET qr_code = qr_text,
        qr_created_at = CURRENT_TIMESTAMP
    WHERE ID_Paciente = p_id_paciente;
    
    RETURN qr_text;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener datos del paciente por QR
CREATE OR REPLACE FUNCTION get_patient_by_qr(p_qr_code TEXT)
RETURNS TABLE (
    nhc TEXT,
    nombre_completo TEXT,
    diagnostico_actual TEXT,
    qr_code TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.NHC,
        p.Nombre || ' ' || p.Apellidos,
        d.Tipo_MPDI,
        p.qr_code
    FROM Paciente p
    JOIN Diagnostico d ON p.ID_Paciente = d.ID_Paciente
    WHERE p.qr_code = p_qr_code AND d.Activo = true;
END;
$$ LANGUAGE plpgsql;

-- Ejemplo de uso:
-- SELECT generate_patient_qr(1); -- Generar QR para paciente con ID 1
-- SELECT * FROM get_patient_by_qr('PAT-1-1234567890-123'); -- Buscar paciente por QR
