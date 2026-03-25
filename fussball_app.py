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


st.divider()
st.subheader("🤝 Werde Teil der Community")

with st.form("community_input"):
    name = st.text_input("Dein Name / Verein")
    idee = st.text_area("Welche Übung fehlt dir? Oder teile einen Tipp:")
    submit = st.form_submit_button("Vorschlag einsenden")
    
    if submit:
        # Hier speichern wir es für den Anfang einfach in einer Liste oder zeigen es an
        st.success(f"Danke {name}! Dein Vorschlag wurde an die 'Taktikkabine' gesendet.")
        # Später: Hier wird der Input in eine Datenbank geschrieben
