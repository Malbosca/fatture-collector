import webbrowser
from datetime import datetime
from urllib.parse import quote

def create_reminder():
    title = "Invia fatture al commercialista"
    details = "Apri Fatture Collector e invia le fatture mensili"
    
    # Link per creare evento ricorrente su Google Calendar
    url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={quote(title)}&details={quote(details)}&recur=RRULE:FREQ=MONTHLY;BYMONTHDAY=1"
    
    webbrowser.open(url)
    print("Aperto Google Calendar - salva l'evento!")

if __name__ == "__main__":
    create_reminder()
