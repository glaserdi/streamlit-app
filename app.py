import streamlit as st
import termok
import vagott_uvegek
import pandas as pd
from streamlit_calendar import calendar
import tusolofulkek

# Sidebar navigáció
st.set_page_config(layout="wide")
st.sidebar.title("Navigáció")
page = st.sidebar.radio("Válassz egy oldalt:", ["Főoldal", "Termó számítások", "Vágott üveg számítások", "Tusolófülke számítások"])

# Oldalak betöltése
if page == "Főoldal":
    st.title("📆 Határidő Naptár")

    # Fájl betöltése
    file_path = "./deadlines.csv"
    try:
        df = pd.read_csv(file_path)
        df["start"] = pd.to_datetime(df["start"], errors="coerce")

        # Ellenőrizzük, hogy nincs-e rossz dátum
        df = df.dropna(subset=["start"])

        # Streamlit Calendar események létrehozása
        events = [{"title": row["title"], "start": row["start"].strftime("%Y-%m-%d")} for _, row in df.iterrows()]

        # Naptár megjelenítése
        calendar(events)

    except Exception as e:
        st.error(f"Hiba történt az adatok beolvasása közben: {e}")


    # Határidők betöltése
    def load_deadlines():
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            return pd.DataFrame(columns=["title", "start"])


    deadlines = load_deadlines()

    st.title("Határidő Kezelő")

    # 🔹 Határidők listázása és egyenkénti törlése
    if not deadlines.empty:
        selected_deadline = st.selectbox("Válassz egy határidőt törlésre:", deadlines["title"])
        if st.button("Kiválasztott határidő törlése"):
            deadlines = deadlines[deadlines["title"] != selected_deadline]  # Kiválasztott törlése
            deadlines.to_csv(file_path, index=False)
            st.success(f"✅ '{selected_deadline}' törölve!")
            st.rerun()
    else:
        st.info("Nincsenek határidők.")

    # 🔹 Összes határidő törlése
    if not deadlines.empty and st.button("Összes határidő törlése"):
        deadlines = pd.DataFrame(columns=["title", "start"])
        deadlines.to_csv(file_path, index=False)
        st.warning("🗑️ Minden határidő törölve!")
        st.rerun()

elif page == "Termó számítások":
    termok.show()

elif page == "Vágott üveg számítások":
    vagott_uvegek.show()

elif page == "Tusolófülke számítások":
    tusolofulkek.show()
