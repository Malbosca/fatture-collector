from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"
OUTPUT_DIR = BASE_DIR / "fatture_scaricate"

oggi = datetime.now()
primo_mese_corrente = oggi.replace(day=1)
INIZIO_PERIODO = (primo_mese_corrente - timedelta(days=1)).replace(day=1)
FINE_PERIODO = primo_mese_corrente - timedelta(days=1)

EMAIL_COMMERCIALISTA = "a.blogna@stcom.info"

MITTENTI_FATTURE = [
    "contact@t.brevo.com",
    "invoice+statements+acct_152gHsF8zEQmD9T4@stripe.com",
    "help@paddle.com",
    "mailer@fastspring.com",
    "noreply@stripe.com",
    "service@paypal.it",
    "no-reply@sumup.com",
    "auto-confirm@amazon.it",
    "payments@amazon.it",
]
