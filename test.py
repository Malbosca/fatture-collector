print("1. Inizio test")

try:
    from config import CREDENTIALS_FILE
    print(f"2. Config OK: {CREDENTIALS_FILE}")
except Exception as e:
    print(f"2. Errore config: {e}")

try:
    from collectors.gmail import collect
    print("3. Import gmail OK")
except Exception as e:
    print(f"3. Errore import gmail: {e}")

print("4. Lancio collect...")
try:
    collect()
except Exception as e:
    print(f"5. Errore collect: {e}")
