import qrcode
from io import BytesIO
import base64
from supabase import create_client, Client
from datetime import datetime

# Supabase configuration
SUPABASE_URL = "https://supdrzpdynaekvysaeio.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN1cGRyenBkeW5hZWt2eXNhZWlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQxODQzNjAsImV4cCI6MjA0OTc2MDM2MH0.PpDKwNEUt2l5h2rISdhjgjShzKijozx_dmnKoLFFSMM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_qr_code(patient_id: int) -> str:
    """Generate QR code for a patient and return as base64 string"""
    try:
        # Call the SQL function to generate QR text
        response = supabase.rpc('generate_patient_qr', {'p_id_paciente': patient_id}).execute()
        qr_text = response.data

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)

        # Create QR image
        img_buffer = BytesIO()
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(img_buffer, format='PNG')
        
        # Convert to base64
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generating QR: {str(e)}")
        return None

def verify_qr_code(qr_code: str) -> dict:
    """Verify QR code and return patient data"""
    try:
        response = supabase.rpc('get_patient_by_qr', {'p_qr_code': qr_code}).execute()
        return response.data
    except Exception as e:
        print(f"Error verifying QR: {str(e)}")
        return None

def get_patient_history(nhc: str) -> dict:
    """Get patient's medical history"""
    try:
        response = supabase.rpc('obtener_historia_clinica', {'p_nhc': nhc}).execute()
        return response.data
    except Exception as e:
        print(f"Error getting history: {str(e)}")
        return None
