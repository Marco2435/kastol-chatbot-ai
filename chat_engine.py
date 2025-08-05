from datetime import datetime

import streamlit as st
import os
import joblib
ml_model = None
if os.path.exists('ml_training/model.pkl'):
    ml_model = joblib.load('ml_training/model.pkl')
from rl.reward_model import log_reward
from monitoring.anomaly_detector import AnomalyDetector, log_anomalie
import os
anomaly_detector = AnomalyDetector()
if os.path.exists('logs/clickstream.csv'):
    with open('logs/clickstream.csv', 'r', encoding='utf-8') as f:
        vragen = [r.split(',')[5] for i, r in enumerate(f.readlines()) if i > 0]
    if vragen:
        anomaly_detector.fit(vragen)
from utils.clickstream_logger import registreer_click
from utils.env_loader import load_environment
from ingestion.file_router import load_all_files, load_uploaded_files
from processing.fuzzy_search import fuzzy_search
from fuzzywuzzy import fuzz
from processing.context_indexer import zoek_relevante_context
from processing.fuzzy_search import fuzzy_search
from fuzzywuzzy import fuzz
from processing.context_trimmer import trim_context
from feedback.feedback_loop import sla_feedback_op
from notifications.email_notifier import stuur_email
from groq_api import vraag_aan_groq

load_environment()

st.set_page_config(page_title="Kastol AI Chatbot", layout="centered")

# Sidebar - Taal en Upload
st.sidebar.header("Instellingen")
taal = st.sidebar.selectbox("Taalkeuze", ["NL", "EN", "DE", "FR"], index=0)
uploaded = st.sidebar.file_uploader("Upload je bestanden", accept_multiple_files=True,
                                     type=["pdf", "docx", "xlsx", "csv", "json", "html"])

# Tabs bovenin
tab1, tab2 = st.tabs(["💬 Chat", "📊 Feedback"])

with tab1:
    st.title("Kastol AI Chatbot")
    st.markdown("Stel hier je technische vraag. De AI gebruikt documenten uit de 'data' map en uploads uit de sidebar.")

    if 'geschiedenis' not in st.session_state:
        st.session_state.geschiedenis = []
    vraag = st.text_input("Wat wil je weten?")
    context = load_all_files()
    if uploaded:
        context += "\n" + load_uploaded_files(uploaded)

    if vraag:
        gefilterde_context = zoek_relevante_context(vraag)
        fuzzy_info = ''
        if not gefilterde_context:
            from ingestion.file_router import route_all_files
            context_lijst = route_all_files()
            kandidaten = []
            for blok in context_lijst:
                score = fuzz.partial_ratio(vraag.lower(), blok.lower())
                if score >= 70:
                    kandidaten.append((score, blok))
            kandidaten.sort(reverse=True)
            if kandidaten:
                score, top = kandidaten[0]
                gefilterde_context = top
                fuzzy_info = f"_Fuzzy match gevonden (score: {score}%)_\n\n"
        if not gefilterde_context:
            gefilterde_context = fuzzy_search(vraag, context_lijst)
        getrimde_context = trim_context(gefilterde_context)
        antwoord = vraag_aan_groq(vraag, getrimde_context, taal)
        if antwoord:
            st.markdown("**Antwoord:**")
            st.markdown("---")
            st.markdown("### 📜 Vorige vragen deze sessie:")
            st.markdown('---')
            from feedback.feedback_loop import registreer_feedback
            col1, col2 = st.columns(2)
            with col1:
                if st.button('👍 Goed antwoord'):
                    log_reward(vraag, antwoord, score=1)
                    registreer_feedback(vraag, antwoord, 'positief')
                    st.success('Bedankt voor je feedback!')
            with col2:
                if st.button('👎 Slecht antwoord'):
                    log_reward(vraag, antwoord, score=-1)
                    registreer_feedback(vraag, antwoord, 'negatief')
                    st.warning('We registreren dit voor verbetering.')
                    verbeterd = st.text_area('Wat had het juiste antwoord moeten zijn?')
                    if verbeterd:
                        from feedback.feedback_loop import registreer_verbeterde_feedback
                        log_reward(vraag, antwoord, verbeterd, score=0.5)
                        registreer_verbeterde_feedback(vraag, antwoord, verbeterd)
                        st.success('Dank je! Dit wordt gebruikt voor AI-training.')
            st.markdown('### 📧 E-mail ontvangen van deze sessie?')
            st.markdown('---')
            from utils.pdf_generator import maak_chat_pdf
            if st.button('📄 Genereer PDF van dit gesprek'):
                pad = maak_chat_pdf(st.session_state.geschiedenis, taal)

with open(pad, 'rb') as pdf_file:
    registreer_click('download_pdf')
    st.download_button('Download PDF', pdf_file, file_name=os.path.basename(pad))
            email_ontvanger = st.text_input('Vul je e-mailadres in:')
        registreer_click('stuur_email')
            if st.button('Stuur sessie per e-mail') and email_ontvanger:
                inhoud = ''
                for item in st.session_state.geschiedenis:
                    inhoud += f"🕓 {item['tijd']}\nVraag: {item['vraag']}\nAntwoord: {item['antwoord']}\n\n"
                from notifications.email_notifier import stuur_email_naar_gebruiker
                if stuur_email_naar_gebruiker(email_ontvanger, inhoud):
                    st.success('E-mail succesvol verzonden.')
                else:
                    st.error('Fout bij verzenden e-mail.')
            for item in reversed(st.session_state.geschiedenis[:-1]):
                st.markdown(f"🕓 *{item['tijd']}*")
                st.markdown(f"**Vraag:** {item['vraag']}")
                st.markdown(f"**Antwoord:** {item['antwoord']}")
                st.markdown("---")
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            st.session_state.geschiedenis.append({'vraag': vraag, 'antwoord': antwoord, 'tijd': timestamp})
            st.success(antwoord)

            # Feedback
            st.markdown("Geef feedback op het antwoord:")
            st.markdown('---')
            st.button('👍 Goed antwoord', on_click=lambda: sla_feedback_op(vraag, antwoord, 'positief'))
            st.button('👎 Slecht antwoord', on_click=lambda: [sla_feedback_op(vraag, antwoord, 'negatief'), stuur_email(vraag, antwoord)])
            with col1:
                if st.button("👍 Goed antwoord"):
                    sla_feedback_op(vraag, antwoord, "positief")
            with col2:
                if st.button("👎 Slecht antwoord"):
                    sla_feedback_op(vraag, antwoord, "negatief")
                    stuur_email(vraag, antwoord)

with tab2:
    st.header("Feedbackoverzicht")
    st.markdown("Alle feedback wordt opgeslagen in `feedback/feedback.csv`. Bekijk het bestand in GitHub of lokaal.")
