import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
import shutil
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
    EMAIL_COMMERCIALISTA = "a.blogna@stcom.info"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

ARCHIVIO_BASE = Path.home() / "Documents" / "malbosca" / "1_FATTURE" / "FATTURE_estere"

MESI_IT = {
    1: "Gennaio", 2: "Febbraio", 3: "Marzo", 4: "Aprile",
    5: "Maggio", 6: "Giugno", 7: "Luglio", 8: "Agosto",
    9: "Settembre", 10: "Ottobre", 11: "Novembre", 12: "Dicembre"
}

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
    msg["Subject"] = f"Fatture {MESI_IT[INIZIO_PERIODO.month]} {INIZIO_PERIODO.year}"
    
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
    
    # Archivia in locale
    anno = str(INIZIO_PERIODO.year)
    mese = f"{INIZIO_PERIODO.month:02d}_{MESI_IT[INIZIO_PERIODO.month]}"
    archivio_dir = ARCHIVIO_BASE / anno / mese
    archivio_dir.mkdir(parents=True, exist_ok=True)
    
    for pdf in pdf_files:
        shutil.copy(pdf, archivio_dir / pdf.name)
    print(f"Archiviati in: {archivio_dir}")
    
    # Pulisci cartella
    for pdf in pdf_files:
        pdf.unlink()
    print("Cartella pulita")

if __name__ == "__main__":
    send()
