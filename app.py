import streamlit as st
from pathlib import Path
from collectors.gmail import collect as gmail_collect
from collectors.checker import check_avvisi
from sender import send
from config import OUTPUT_DIR, INIZIO_PERIODO, FINE_PERIODO

st.set_page_config(
    page_title="Fatture Collector", 
    page_icon="invoice",
    layout="centered"
)

st.markdown('''
<style>
    .main-title { text-align: center; color: #2E7D32; font-size: 2.5rem; margin-bottom: 0; }
    .subtitle { text-align: center; color: #666; font-size: 1rem; margin-bottom: 2rem; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 1rem; text-align: center; color: white; margin-bottom: 2rem; }
    .metric-number { font-size: 3rem; font-weight: bold; }
    .metric-label { font-size: 1rem; opacity: 0.9; }
    .warning-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
</style>
''', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Fatture Collector</h1>', unsafe_allow_html=True)
periodo = f"{INIZIO_PERIODO.strftime('%B %Y')}"
st.markdown(f'<p class="subtitle">Periodo: {periodo}</p>', unsafe_allow_html=True)

# Controllo avvisi fatture
try:
    avvisi = check_avvisi()
    if avvisi:
        for a in avvisi:
            st.warning(f"**{a['nome']}**: {a['count']} fattura/e da scaricare manualmente!")
except Exception as e:
    pass

OUTPUT_DIR.mkdir(exist_ok=True)
pdf_files = list(OUTPUT_DIR.glob("*.pdf"))
pdf_count = len(pdf_files)

st.markdown(f'''
<div class="metric-card">
    <div class="metric-number">{pdf_count}</div>
    <div class="metric-label">PDF pronti per l'invio</div>
</div>
''', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("Scarica da Gmail", use_container_width=True):
        with st.spinner("Scaricando fatture..."):
            for f in OUTPUT_DIR.glob("*.pdf"):
                f.unlink()
            results = gmail_collect()
        st.success(f"Scaricati {len(results)} PDF!")
        st.rerun()

with col2:
    with st.popover("Dashboard", use_container_width=True):
        st.markdown("[Stripe](https://dashboard.stripe.com/settings/documents)")
        st.markdown("[PayPal](https://www.paypal.com/reports/statements)")
        st.markdown("[SumUp](https://me.sumup.com/invoices)")
        st.markdown("[Amazon](https://sellercentral.amazon.it/tax/seller-fee-invoices)")
        st.markdown("[Canva](https://www.canva.com/settings/purchase-history)")

uploaded = st.file_uploader("Carica altri PDF", type="pdf", accept_multiple_files=True)
if uploaded:
    for file in uploaded:
        filepath = OUTPUT_DIR / file.name
        filepath.write_bytes(file.read())
    st.success(f"Caricati {len(uploaded)} PDF!")
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.button("INVIA AL COMMERCIALISTA", use_container_width=True, type="primary"):
    if pdf_count == 0:
        st.error("Nessun PDF da inviare!")
    else:
        with st.spinner("Invio email in corso..."):
            send()
        st.success("Email inviata con successo!")
        st.balloons()

if pdf_count > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Documenti")
    for pdf in pdf_files:
        st.markdown(f"- {pdf.name}")
