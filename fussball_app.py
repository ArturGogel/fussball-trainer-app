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
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATEN LADEN & FEHLERABFANG ---
@st.cache_data
def load_data():
    try:
        # Wir laden die CSV
        df = pd.read_csv("uebungen.csv")
        # Alle Spaltennamen von Leerzeichen befreien (Sicherheitscheck)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

df = load_data()

# --- 4. SEITENLEISTE (NAVIGATION) ---
with st.sidebar:
    st.title("⚽ CoachFlow")
    st.subheader("Menü")
    
    if df is not None:
        jugend_list = ["Alle"] + sorted(df['jugend'].unique().tolist())
        auswahl = st.selectbox("Altersklasse filtern:", jugend_list)
    else:
        auswahl = "Alle"
        st.error("Datei 'uebungen.csv' wurde nicht gefunden!")

    st.markdown("---")
    st.write("**Status:** 🟢 Online")
    st.caption("Version 1.2 | Social Beta")

# --- 5. HAUPTBEREICH ---
st.title("Deine Trainings-Bibliothek")

if df is not None:
    # Filter anwenden
    if auswahl != "Alle":
        gefiltert = df[df['jugend'] == auswahl]
    else:
        gefiltert = df

    # Anzeige in einem 2-Spalten-Grid
    cols = st.columns(2)
    
    for i, (index, row) in enumerate(gefiltert.iterrows()):
        with cols[i % 2]:
            # Jede Übung in einer "Card" (Expander)
            with st.expander(f"**{row['titel']}** ({row['jugend']})"):
                
                # --- BILD-CHECK (Hier war der Fehler!) ---
                # Wir prüfen erst, ob die Spalte 'bild' überhaupt im Dokument existiert
                if 'bild' in row and pd.notnull(row['bild']) and str(row['bild']).strip() != "":
                    bild_pfad = str(row['bild']).strip()
                    if os.path.exists(bild_pfad):
                        st.image(bild_pfad, use_container_width=True)
                    else:
                        st.info(f"📸 Skizze für '{row['titel']}' wird bald hochgeladen.")
                
                # Details zur Übung
                st.markdown(f"**Übung:** {row['inhalt']}")
                st.info(f"💡 **Coaching:** {row['coaching']}")
                
                # WhatsApp-Integration
                wa_text = f"Heute Training ({row['jugend']}):\n*{row['titel']}*\n{row['inhalt']}\n\nBis später! ⚽"
                wa_link = f"https://wa.me/?text={urllib.parse.quote(wa_text)}"
                st.link_button("📲 Per WhatsApp teilen", wa_link)

else:
    st.warning("Bitte stelle sicher, dass die Datei 'uebungen.csv' im selben Ordner auf GitHub liegt.")

# --- 6. COMMUNITY-FEEDBACK (SOCIAL ANSATZ) ---
st.divider()
with st.container():
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("Fehlt dir eine Übung?")
       wunsch = st.text_input("Welches Thema brauchst du als nächstes?", placeholder="z.B. Kopfballspiel U13")
    with col_b:
        st.write("###") # Abstandhalter
        if st.button("Anfrage senden"):
            st.toast("Wunsch wurde gespeichert! ⭐")
