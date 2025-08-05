
import csv
import os
from datetime import datetime
import uuid

logpad = "logs/clickstream.csv"

def registreer_click(actie, inhoud="", taal="", vraag="", antwoord=""):
    sessie_id = get_session_id()
    regel = [sessie_id, datetime.now().isoformat(), actie, inhoud, taal, vraag, antwoord]
    bestaat = os.path.exists(logpad)
    with open(logpad, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not bestaat:
            writer.writerow(["sessie_id", "tijd", "actie", "inhoud", "taal", "vraag", "antwoord"])
        writer.writerow(regel)

def get_session_id():
    import streamlit as st
    if "sessie_id" not in st.session_state:
        st.session_state.sessie_id = str(uuid.uuid4())
    return st.session_state.sessie_id
