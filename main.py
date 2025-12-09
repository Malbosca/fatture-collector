from pathlib import Path
from collectors.gmail import collect as gmail_collect
from sender import send
from config import OUTPUT_DIR

def main():
    print("=== FATTURE COLLECTOR ===\n")
    
    # Pulisci cartella
    if OUTPUT_DIR.exists():
        for f in OUTPUT_DIR.glob("*.pdf"):
            f.unlink()
        print(f"Cartella pulita\n")
    
    # Raccogli da Gmail
    gmail_collect()
    
    # Invia al commercialista
    print("\n")
    send()
    
    print("\n=== COMPLETATO ===")

if __name__ == "__main__":
    main()
