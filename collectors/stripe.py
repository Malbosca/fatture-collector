from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import time
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import OUTPUT_DIR

STRIPE_EMAIL = "tua@email.com"
STRIPE_PASSWORD = "tua_password"

def collect():
    print("Stripe Collector (Browser)")
    print("=" * 40)
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": str(OUTPUT_DIR.absolute())}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        driver.get("https://dashboard.stripe.com/login")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        driver.find_element(By.NAME, "email").send_keys(STRIPE_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(STRIPE_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        time.sleep(5)  # Attendi login
        
        driver.get("https://dashboard.stripe.com/settings/documents")
        time.sleep(3)
        
        # Cerca link PDF e scarica
        pdf_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Download")
        print(f"Trovati {len(pdf_links)} documenti")
        
        for link in pdf_links:
            link.click()
            time.sleep(2)
        
        print("Download completati")
        
    finally:
        driver.quit()
    
    return list(OUTPUT_DIR.glob("*.pdf"))

if __name__ == "__main__":
    collect()
