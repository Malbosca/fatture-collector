import webbrowser
import time

DASHBOARD_URLS = [
    ("Stripe", "https://dashboard.stripe.com/settings/documents"),
    ("PayPal", "https://www.paypal.com/reports/statements"),
    ("SumUp", "https://me.sumup.com/invoices"),
    ("Amazon", "https://sellercentral.amazon.it/tax/seller-fee-invoices"),
]

def open_all():
    print("Apro le dashboard...")
    print("=" * 40)
    for name, url in DASHBOARD_URLS:
        print(f"  -> {name}")
        webbrowser.open(url)
        time.sleep(1)
    print("\nScarica i PDF nella cartella 'fatture_scaricate'")
    print("Poi lancia: python sender.py")

if __name__ == "__main__":
    open_all()
