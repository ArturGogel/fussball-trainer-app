import streamlit as st
import pandas as pd
import urllib.parse
import os

# --- 1. SEITEN-EINSTELLUNGEN ---
st.set_page_config(page_title="CoachFlow | Taktikkabine", page_icon="⚽", layout="wide")

# --- 2. MODERNES DESIGN (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stExpander { border: 1px solid #d1d5db; border-radius: 12px; background-color: white !important; margin-bottom: 10px; }
    .stButton>button { border-radius: 8px; font-weight: bold; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATEN LADEN ---
@st.cache_data
def load_data():
    try:
        if os.path.exists("uebungen.csv"):
            df = pd.read_csv("uebungen.csv")
            df.columns = df.columns.str.strip()
            return df
        else:
            return None
    except Exception as e:
        return None

df = load_data()

# --- 4. SEITENLEISTE ---
with st.sidebar:
    st.title("⚽ CoachFlow")
    st.subheader("Navigation")
    
    if df is not None:
        jugend_list = ["Alle"] + sorted(df['jugend'].unique().tolist())
        auswahl = st.selectbox("Altersklasse filtern:", jugend_list)
    else:
        auswahl = "Alle"
        st.error("Datei 'uebungen.csv' fehlt!")

    st.markdown("---")
    st.write("**Status:** 🟢 Online")

# --- 5. HAUPTBEREICH ---
st.title("Deine Trainings-Bibliothek")

if df is not None:
    if auswahl != "Alle":
        gefiltert = df[df['jugend'] == auswahl]
    else:
        gefiltert = df

    # Anzeige in 2 Spalten
    cols = st.columns(2)
    
    for i, (index, row) in enumerate(gefiltert.iterrows()):
        with cols[i % 2]:
            with st.expander(f"**{row['titel']}** ({row['jugend']})"):
                
                # BILD-CHECK
                if 'bild' in row and pd.notnull(row['bild']) and str(row['bild']).strip() != "":
                    bild_name = str(row['bild']).strip()
                    if os.path.exists(bild_name):
                        st.image(bild_name, use_container_width=True)
                    else:
                        st.info(f"📸 Skizze folgt für: {row['titel']}")
                
                st.markdown(f"**Übung:** {row['inhalt']}")
                st.info(f"💡 **Coaching:** {row['coaching']}")
                
                # WhatsApp Button
                wa_text = f"Heute Training ({row['jugend']}):\n*{row['titel']}*\n{row['inhalt']}"
                wa_link = f"https://wa.me/?text={urllib.parse.quote(wa_text)}"
                st.link_button("📲 Per WhatsApp teilen", wa_link)
else:
    st.warning("Keine Daten gefunden. Bitte uebungen.csv hochladen.")

# --- 6. COMMUNITY-FEEDBACK ---
st.divider()
st.subheader("🤝 Feedback & Wünsche")
col_a, col_b = st.columns([2, 1])

with col_a:
    wunsch = st.text_input("Welches Thema fehlt dir?", placeholder="z.B. Kopfballspiel U13")

with col_b:
    st.write("###") 
    if st.button("Anfrage senden"):
        if wunsch:
            st.toast(f"Wunsch '{wunsch}' vorgemerkt! ⭐")
        else:
            st.warning("Bitte gib erst etwas ein.")
