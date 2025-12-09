import streamlit as st
from pathlib import Path
from collectors.gmail import collect as gmail_collect
from sender import send
from config import OUTPUT_DIR, INIZIO_PERIODO, FINE_PERIODO
import webbrowser

st.set_page_config(
    page_title="Fatture Collector", 
    page_icon="invoice",
    layout="centered"
)

# CSS custom
st.markdown('''
<style>
    .main-title {
        text-align: center;
        color: #2E7D32;
        font-size: 2.5rem;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-number {
        font-size: 3rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .stButton > button {
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-weight: 500;
    }
    .pdf-list {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .pdf-item {
        padding: 0.5rem;
        border-bottom: 1px solid #eee;
    }
</style>
''', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Fatture Collector</h1>', unsafe_allow_html=True)
periodo = f"{INIZIO_PERIODO.strftime('%B %Y')}"
st.markdown(f'<p class="subtitle">Periodo: {periodo}</p>', unsafe_allow_html=True)

# Conteggio PDF
if OUTPUT_DIR.exists():
    pdf_files = list(OUTPUT_DIR.glob("*.pdf"))
    pdf_count = len(pdf_files)
else:
    pdf_files = []
    pdf_count = 0

# Metric card
st.markdown(f'''
<div class="metric-card">
    <div class="metric-number">{pdf_count}</div>
    <div class="metric-label">PDF pronti per l'invio</div>
</div>
''', unsafe_allow_html=True)

# Bottoni
col1, col2 = st.columns(2)

with col1:
    if st.button("Scarica da Gmail", use_container_width=True):
        with st.spinner("Scaricando fatture..."):
            if OUTPUT_DIR.exists():
                for f in OUTPUT_DIR.glob("*.pdf"):
                    f.unlink()
            results = gmail_collect()
        st.success(f"Scaricati {len(results)} PDF!")
        st.rerun()

with col2:
    if st.button("Apri Dashboard", use_container_width=True):
        urls = [
            "https://dashboard.stripe.com/settings/documents",
            "https://www.paypal.com/reports/statements",
            "https://me.sumup.com/invoices",
            "https://sellercentral.amazon.it/tax/seller-fee-invoices",
        ]
        for url in urls:
            webbrowser.open(url)
        st.info("Dashboard aperte nel browser!")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("INVIA AL COMMERCIALISTA", use_container_width=True, type="primary"):
    if pdf_count == 0:
        st.error("Nessun PDF da inviare!")
    else:
        with st.spinner("Invio email in corso..."):
            send()
        st.success("Email inviata con successo!")
        st.balloons()

# Lista PDF
if pdf_count > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Documenti")
    for pdf in pdf_files:
        st.markdown(f"- {pdf.name}")
