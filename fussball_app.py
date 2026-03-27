import streamlit as st
import pandas as pd
import urllib.parse
import os

# --- PAGE CONFIG (Muss ganz oben stehen!) ---
st.set_page_config(page_title="CoachFlow | Die Taktikkabine", page_icon="⚽", layout="wide")

# --- CUSTOM CSS (Für den modernen Look) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stExpander { border: 1px solid #e6e9ef; border-radius: 10px; background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Navigation & Filter) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/football.png", width=80) # Platzhalter für dein Logo
    st.title("CoachFlow")
    st.markdown("---")
    st.subheader("Filter")
    
    # Daten laden
    try:
        df = pd.read_csv("uebungen.csv")
        alle_jugenden = df['jugend'].unique()
        auswahl = st.selectbox("Altersklasse wählen", ["Alle"] + list(alle_jugenden))
    except:
        st.error("Datenbank nicht gefunden.")
        df = pd.DataFrame()

    st.markdown("---")
    st.info("💡 **Tipp:** Nutze die Skizzen, um sie deinen Spielern direkt auf dem Tablet zu zeigen.")

# --- HAUPTBEREICH ---
st.title("⚽ Deine Trainings-Bibliothek")
st.write(f"Aktuelle Auswahl: **{auswahl}**")

if not df.empty:
    # Filter Logik
    if auswahl != "Alle":
        gefiltert = df[df['jugend'] == auswahl]
    else:
        gefiltert = df

    # Layout mit Spalten für die Übungen (2 Spalten)
    cols = st.columns(2)
    
    for i, (index, row) in enumerate(gefiltert.iterrows()):
        # Abwechselnd in linke und rechte Spalte schreiben
        with cols[i % 2]:
            with st.container():
                with st.expander(f"**{row['titel']}**", expanded=False):
                    # Bild-Anzeige
                    # --- SICHERE BILD-ANZEIGE ---
                    if 'bild' in row and pd.notnull(row['bild']) and row['bild'] != "":
                    if os.path.exists(row['bild']):
                        st.image(row['bild'], use_container_width=True)
                    else:
                        st.info(f"📸 Skizze folgt in Kürze für: {row['titel']}")
                    
                    st.markdown(f"**Anforderung:** {row['inhalt']}")
                    st.success(f"**Coach-Voice:** {row['coaching']}")
                    
                    # WhatsApp Button
                    text = f"Training heute ({row['jugend']}):\n*{row['titel']}*\n{row['inhalt']}"
                    link = f"https://wa.me/?text={urllib.parse.quote(text)}"
                    st.link_button(f"📲 An Team senden", link)
else:
    st.warning("Noch keine Übungen hinterlegt. Erstelle eine 'uebungen.csv' auf GitHub.")

# --- FOOTER ---
st.divider()
st.caption("© 2026 CoachFlow - Das Netzwerk für ambitionierte Trainer")
