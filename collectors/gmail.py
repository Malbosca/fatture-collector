import base64
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import streamlit as st

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import OUTPUT_DIR, INIZIO_PERIODO, FINE_PERIODO, MITTENTI_FATTURE

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service():
    if 'google' in st.secrets:
        creds = Credentials(
            token=st.secrets['google']['token'],
            refresh_token=st.secrets['google']['refresh_token'],
            token_uri=st.secrets['google']['token_uri'],
            client_id=st.secrets['google']['client_id'],
            client_secret=st.secrets['google']['client_secret'],
            scopes=SCOPES
        )
        if not creds.valid:
            creds.refresh(Request())
    else:
        from config import TOKEN_FILE
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        if not creds.valid and creds.refresh_token:
            creds.refresh(Request())
    return build('gmail', 'v1', credentials=creds)


def build_query():
    after = INIZIO_PERIODO.strftime("%Y/%m/%d")
    before = FINE_PERIODO.strftime("%Y/%m/%d")
    mittenti = " OR ".join([f"from:{m}" for m in MITTENTI_FATTURE])
    query = f"has:attachment after:{after} before:{before} ({mittenti})"
    print(f"Query Gmail: {query}")
    return query


def download_attachments(service, message_id, save_dir):
    msg = service.users().messages().get(userId='me', id=message_id).execute()
    downloaded = []
    parts = msg.get('payload', {}).get('parts', [])
    for part in parts:
        filename = part.get('filename', '')
        if not filename.lower().endswith('.pdf'):
            continue
        attachment_id = part.get('body', {}).get('attachmentId')
        if not attachment_id:
            continue
        attachment = service.users().messages().attachments().get(
            userId='me', messageId=message_id, id=attachment_id
        ).execute()
        data = base64.urlsafe_b64decode(attachment['data'])
        filepath = save_dir / filename
        counter = 1
        while filepath.exists():
            filepath = save_dir / f"{filepath.stem}_{counter}.pdf"
            counter += 1
        filepath.write_bytes(data)
        downloaded.append(filepath)
        print(f"  Salvato: {filepath.name}")
    return downloaded


def collect():
    print("Gmail Collector")
    print("=" * 40)
    OUTPUT_DIR.mkdir(exist_ok=True)
    service = get_gmail_service()
    query = build_query()
    results = service.users().messages().list(
        userId='me', q=query, maxResults=100
    ).execute()
    messages = results.get('messages', [])
    print(f"Trovate {len(messages)} email con potenziali fatture")
    all_downloaded = []
    for msg in messages:
        downloaded = download_attachments(service, msg['id'], OUTPUT_DIR)
        all_downloaded.extend(downloaded)
    print(f"Totale PDF scaricati: {len(all_downloaded)}")
    return all_downloaded


if __name__ == "__main__":
    collect()
