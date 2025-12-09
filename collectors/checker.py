from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import INIZIO_PERIODO, FINE_PERIODO

try:
    import streamlit as st
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = Credentials(
        token=st.secrets['google']['token'],
        refresh_token=st.secrets['google']['refresh_token'],
        token_uri=st.secrets['google']['token_uri'],
        client_id=st.secrets['google']['client_id'],
        client_secret=st.secrets['google']['client_secret'],
        scopes=SCOPES
    )
except:
    from config import TOKEN_FILE
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

AVVISI_FATTURE = [
    {"nome": "Amazon", "from": "donotreply@amazon.com", "subject": "La tua Fattura Elettronica Venditore Amazon.it per"},
    {"nome": "Stripe", "from": "notifications@stripe.com", "subject": "? disponibile una nuova fattura Malbosca"},
    {"nome": "Canva", "from": "no-reply@account.canva.com", "subject": "Your Canva invoice"},
]

def get_service():
    global creds
    if creds is None:
        from config import TOKEN_FILE
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
    return build('gmail', 'v1', credentials=creds)

def check_avvisi():
    service = get_service()
    after = INIZIO_PERIODO.strftime("%Y/%m/%d")
    before = FINE_PERIODO.strftime("%Y/%m/%d")
    
    risultati = []
    
    for avviso in AVVISI_FATTURE:
        query = f"from:{avviso['from']} subject:\"{avviso['subject']}\" after:{after} before:{before}"
        results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
        count = len(results.get('messages', []))
        if count > 0:
            risultati.append({"nome": avviso['nome'], "count": count})
    
    return risultati

if __name__ == "__main__":
    avvisi = check_avvisi()
    if avvisi:
        for a in avvisi:
            print(f"{a['nome']}: {a['count']} fatture da scaricare")
    else:
        print("Nessuna fattura in attesa")
