import streamlit as st
import pandas as pd
import urllib.parse

st.title("⚽ Trainer-Assistent Pro")

# 1. Daten aus der CSV laden
try:
    df = pd.read_csv("uebungen.csv")
except:
    st.error("Datenbank konnte nicht geladen werden.")
    df = pd.DataFrame()

# 2. Filter für die Jugend
if not df.empty:
    alle_jugenden = df['jugend'].unique()
    auswahl = st.selectbox("Wähle die Altersklasse:", alle_jugenden)

    # 3. Übungen dieser Altersklasse anzeigen
    gefiltert = df[df['jugend'] == auswahl]
    
    for index, row in gefiltert.iterrows():
        with st.expander(f"📋 {row['titel']}"):
            st.write(f"**Ablauf:** {row['inhalt']}")
            st.info(f"💡 **Coaching:** {row['coaching']}")
            
            # WhatsApp Button pro Übung
            text = f"Training heute ({auswahl}):\n*{row['titel']}*\n{row['inhalt']}"
            link = f"https://wa.me/?text={urllib.parse.quote(text)}"
            st.link_button(f"An Team senden", link)
else:
    st.write("Noch keine Übungen in der Datenbank.")
