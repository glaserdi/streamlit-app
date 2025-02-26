import streamlit as st
import rendelesek
import vagott_uvegek
import pandas as pd
from streamlit_calendar import calendar
import tusolofulkek
import kepkeretek
import toml
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import gspread
from google.oauth2.service_account import Credentials
import json
import os
import termok

# Ellenőrizzük, hogy a titok ténylegesen létezik-e
if "GOOGLE_SHEET_CREDENTIALS" in st.secrets:
    google_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]
else:
    raise ValueError("A GOOGLE_SHEET_CREDENTIALS titok nem található!")

# Google Sheets hitelesítés
creds = Credentials.from_service_account_info(google_credentials, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])

client = gspread.authorize(creds)

# A Google Táblázat elérése
SHEET_ID = "1MrOG_Tlti2lWoVtrK8YsVsuI5UIWS8CTRRPVH1LjlEI"
sheet = client.open_by_key(SHEET_ID)



# Streamlit gyorsítótárazás (csak ha nem változik gyakran)
@st.cache_data
def collect_calendar_data():
    worksheet = sheet.worksheet("Határidők")
    df = pd.DataFrame(worksheet.get_all_records())
    return df


def modify_calendar_data(df):
    worksheet = sheet.worksheet("Határidők")

    # 🛠️ Adatok törlése és újraírása
    worksheet.clear()

    # Dátumformázás biztosítása
    df["start"] = pd.to_datetime(df["start"], errors="coerce").dt.strftime("%Y-%m-%d")

    set_with_dataframe(worksheet, df)

# Próbáljuk meg beolvasni a secrets fájlt
try:
    secrets = toml.load(".streamlit/secrets.toml")  # Vagy "config.toml"
    users = secrets.get("users", {})
except Exception as e:
    st.error(f"Hiba a secrets.toml betöltésekor: {e}")
    users = {}


# 📌 Session state inicializálás
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.username_str = None





# 🔐 Bejelentkezési oldal
def login_page():
    st.markdown("## 🔐 Bejelentkezés")
    # Beviteli mezők
    username = st.text_input("Felhasználónév")
    password = st.text_input("Jelszó", type="password")

    if st.button("Bejelentkezés"):
        if username in users and users[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.role = users[username]["role"]
            st.session_state.username = username
            st.session_state.username_str = users[username]["nev"]
            st.success(f"✅ Sikeres bejelentkezés: {st.session_state.username_str}")
            st.rerun()
        else:
            st.error("❌ Hibás felhasználónév vagy jelszó")

# 🏠 **Fő tartalom**
def main_content():

    # 🎛️ Sidebar menü
    st.sidebar.title("Navigáció")

    if st.session_state.role == "admin":
        pages = ["Főoldal", "Termó számítások", "Vágott üveg számítások", "Tusolófülke számítások"]
    elif st.session_state.role in ["glaserdi_fonok", "glaserdi_alkalmazott"]:
        pages = ["Főoldal", "Termó számítások", "Vágott üveg számítások",
                 "Tusolófülke számítások", "Képkeret számítások", "Bejövő rendelések"]
    elif st.session_state.role == "vasarlo":
        pages = ["Termó számítások"]
    else:
        pages = []

    page = st.sidebar.radio("Válassz egy oldalt:", pages)
    
    # 🌟 Felső sávban a kijelentkezés gomb
    if st.session_state.authenticated:
        logout_button = st.button("Kijelentkezés", key="logout_button")
        if logout_button:
            st.session_state.authenticated = False
            st.session_state.role = None
            st.session_state.username = None
            st.session_state.username_str = None
            st.success("✅ Kijelentkezés sikeres.")
            st.experimental_rerun()
        
    if page == "Főoldal":
        st.title("📆 Határidő Naptár")
        deadlines = collect_calendar_data()
        try:
            deadlines["start"] = pd.to_datetime(deadlines["start"], errors="coerce")

            # Ellenőrizzük, hogy nincs-e rossz dátum
            df = deadlines.dropna(subset=["start"])

            # Streamlit Calendar események létrehozása
            events = [{"title": row["title"], "start": row["start"].strftime("%Y-%m-%d")} for _, row in
                      df.iterrows()]

            # Naptár megjelenítése
            calendar(events)

        except Exception as e:
            st.error(f"Hiba történt az adatok beolvasása közben: {e}")

        st.header("✏️ Határidő Módosítása")
        if not deadlines.empty:
            selected_deadline = st.selectbox("Válassz egy határidőt módosításra:", deadlines["title"])
            current_date = deadlines.loc[deadlines["title"] == selected_deadline, "start"].values[0]

            new_date = st.date_input("Új határidő:", pd.to_datetime(current_date))
            new_title = st.text_input("Új név:", selected_deadline, key="new_title")

            if st.button("Módosítás mentése"):
                deadlines.loc[deadlines["title"] == selected_deadline, ["title", "start"]] = [new_title,
                                                                                              new_date.strftime(
                                                                                                  "%Y-%m-%d")]

                modify_calendar_data(deadlines)
                collect_calendar_data.clear()

                st.success(
                    f"✅ '{selected_deadline}' módosítva '{new_title}' névre és új dátuma: {new_date.strftime('%Y-%m-%d')}!")
                st.rerun()

        st.header("🗑️ Határidő törlése")
        if not deadlines.empty:
            selected_deadline = st.selectbox("Válassz egy határidőt törlésre:", deadlines["title"])

            if st.button("Kiválasztott határidő törlése"):
                deadlines = deadlines[deadlines["title"] != selected_deadline]
                modify_calendar_data(deadlines)
                st.success(f"✅ '{selected_deadline}' törölve!")
                st.rerun()
        else:
            st.info("Nincsenek határidők.")

    elif page == "Termó számítások":
        termok.show(st.session_state.role, st.session_state.username_str)

    elif page == "Vágott üveg számítások":
        vagott_uvegek.show()

    elif page == "Tusolófülke számítások":
        tusolofulkek.show()

    elif page == "Képkeret számítások":
        kepkeretek.show()

    elif page == "Bejövő rendelések":
        rendelesek.show()

# 🔥 **Fő programlogika**
if not st.session_state.authenticated:
    login_page()
else:
    main_content()
