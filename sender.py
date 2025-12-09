import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))
from config import OUTPUT_DIR, INIZIO_PERIODO, FINE_PERIODO

try:
    import streamlit as st
    SMTP_EMAIL = st.secrets['smtp']['email']
    SMTP_PASSWORD = st.secrets['smtp']['password']
    EMAIL_COMMERCIALISTA = st.secrets['commercialista']['email']
except:
    SMTP_EMAIL = "aziendamalbosca@gmail.com"
    SMTP_PASSWORD = "ieob mprw fhuj agpj"
    EMAIL_COMMERCIALISTA = "emanuele.visigalli@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send():
    print("Sender")
    print("=" * 40)
    
    pdf_files = list(OUTPUT_DIR.glob("*.pdf"))
    print(f"Trovati {len(pdf_files)} PDF da inviare")
    
    if not pdf_files:
        print("Nessun PDF da inviare")
        return
    
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = EMAIL_COMMERCIALISTA
    msg["Subject"] = f"Fatture {INIZIO_PERIODO.strftime('%B %Y')}"
    
    body = f"In allegato le fatture del periodo {INIZIO_PERIODO.strftime('%d/%m/%Y')} - {FINE_PERIODO.strftime('%d/%m/%Y')}"
    msg.attach(MIMEText(body, "plain"))
    
    for pdf in pdf_files:
        with open(pdf, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={pdf.name}")
            msg.attach(part)
        print(f"  Allegato: {pdf.name}")
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
    
    print(f"\nEmail inviata a {EMAIL_COMMERCIALISTA}")

if __name__ == "__main__":
    send()
