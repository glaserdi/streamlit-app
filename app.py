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
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# AES visszafejtési funkció
def decrypt_password(encrypted_password: str, secret_key: bytes):
    # Az IV és a titkosított jelszó szétválasztása
    iv_b64, encrypted_password_b64 = encrypted_password.split(":")
    
    # Az IV és a titkosított jelszó Base64 dekódolása
    iv = base64.b64decode(iv_b64)
    encrypted_password = base64.b64decode(encrypted_password_b64)
    
    # AES cipher objektum létrehozása a titkosítási kulccsal és az IV-vel
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    
    # Jelszó visszafejtése
    decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size)
    
    return decrypted_password.decode('utf-8')
        
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
    secret_key = base64.b64decode(secrets["SECRET_KEY"])  # Titkosítási kulcs Base64-ből dekódolva
except Exception as e:
    st.error(f"Hiba a secrets.toml betöltésekor: {e}")
    users = {}
    secret_key = None


# 📌 Session state inicializálás
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.username_str = None


def login_page():
    st.markdown("## 🔐 Bejelentkezés")
    # Beviteli mezők
    username = st.text_input("Felhasználónév")
    password = st.text_input("Jelszó", type="password")
# Jelszó ellenőrzése belépéskor

# 🔐 Jelszó ellenőrzés
def check_user_password(username: str, password: str):
    """A beírt jelszó összehasonlítása a titkosított változattal."""
    if username in users:
        encrypted_password = users[username]["password"]
        decrypted_password = decrypt_password(encrypted_password, secret_key)

        if decrypted_password and decrypted_password == password:
            return True
    return False

# 🔑 Bejelentkezési oldal
def login_page():
    st.markdown("## 🔐 Bejelentkezés")

    username = st.text_input("Felhasználónév")
    password = st.text_input("Jelszó", type="password")

    if st.button("Bejelentkezés"):
        if check_user_password(username, password):
            # Bejelentkezési adatok mentése
            st.session_state.authenticated = True
            st.session_state.role = users[username]["role"]
            st.session_state.username = username
            st.session_state.username_str = users[username]["nev"]
            
            st.success(f"✅ Sikeres bejelentkezés: {st.session_state.username_str}")
            st.rerun()
        else:
            st.error("❌ Hibás felhasználónév vagy jelszó!")

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
        pages = ["Termó számítások", "Vágott üveg számítások"]
    else:
        pages = []

    page = st.sidebar.radio("Válassz egy oldalt:", pages)
        
    if page == "Főoldal":
        st.title("📆 Határidő Naptár")
        
        deadlines = collect_calendar_data()
        filtered_deadlines = pd.DataFrame()
        
        try:
            deadlines["start"] = pd.to_datetime(deadlines["start"], errors="coerce")

            # Ellenőrizzük, hogy nincs-e rossz dátum
            df = deadlines.dropna(subset=["start"])

            # Streamlit Calendar események létrehozása
            events = [{"title": row["title"], "start": row["start"].strftime("%Y-%m-%d")} for _, row in
                      df.iterrows()]
            
            # Naptár megjelenítése
            calendar_options = {"initialView": "dayGridMonth",  # Alapértelmezett nézet: havi nézet
                                "firstDay": 1,  # Hétfői kezdés
                                "locale": "hu",  # Magyar nyelv
                                "views": {
                                    "dayGridMonth": {},  # Havi nézet
                                    "listMonth": {}  # Lista nézet
                                },
                                "headerToolbar": {
                                    "left": "prev,next today",  # Előző, következő hónap és 'Ma' gomb
                                    "center": "title",  # Középen a cím
                                    "right": "dayGridMonth,listMonth"  # Nézetválasztó: havi és lista nézet
                                },
                                "height": 800,  # Megnövelt méret
                                "contentHeight": 700
                               }
            if st.button("🔄 Naptár frissítése"):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.rerun()
            calendar(events, options=calendar_options)
    

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
        st.header("➕ Új határidő hozzáadása")
        
        # Beviteli mezők
        uj_megrendeles = st.text_input("Megrendelés neve")
        uj_hatarido = st.date_input("Határidő")
        uj_darabszam = st.number_input("Darabszám", min_value=1, step=1)
        uj_terulet = st.text_input("Terület")
        
        if st.button("Hozzáadás"):
            if uj_megrendeles and uj_hatarido and uj_terulet:
                # Új bejegyzés létrehozása
                new_entry = pd.DataFrame([{
                    "title": uj_megrendeles,
                    "start": uj_hatarido.strftime("%Y-%m-%d"),
                    "Darabszám": uj_darabszam,
                    "Terület": uj_terulet
                }])
        
                # Meglévő adatok lekérése
                deadlines = collect_calendar_data()
        
                # Új adat hozzáfűzése
                deadlines = pd.concat([deadlines, new_entry], ignore_index=True)
        
                # Módosítások mentése a Google Sheets-be
                modify_calendar_data(deadlines)
        
                # Gyorsítótár törlése, hogy a friss adatok megjelenjenek
                collect_calendar_data.clear()
        
                st.success(f"✅ A következő határidő hozzáadva: {uj_megrendeles} - {uj_hatarido.strftime('%Y-%m-%d')}")
                st.rerun()
            else:
                st.error("❌ Minden mezőt ki kell tölteni!")

        
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
            
        st.header("📘 Határidők naplózása")
        if not deadlines.empty:
            selected_day = date = st.date_input("Válassz egy dátumot")
            selected_day_str = selected_day.strftime("%Y-%m-%d")  # Kiválasztott dátumot átalakítjuk stringgé
            deadlines["start"] = pd.to_datetime(deadlines["start"], errors="coerce").dt.strftime("%Y-%m-%d")  # Dátumok formázása
        
            if st.button("Naplózás"):
                # Az adott napra vonatkozó rendelések szűrése
                filtered_deadlines = deadlines[deadlines["start"] == selected_day_str]  # String alapú összehasonlítás
        
                # Ha vannak rendelések, akkor kiírjuk őket
                if not filtered_deadlines.empty:
                    st.write("📅 **Az adott napi rendelések:**")
                    # Oszlopnevek átnevezése egy új DataFrame-ben
                    filtered_display = filtered_deadlines.rename(columns={"title": "Megrendelés neve"})
                    
                    # Csak a kívánt oszlopok megjelenítése az új nevekkel
                    st.dataframe(filtered_display[["Megrendelés neve", "Darabszám", "Terület"]])
                else:
                    st.info("Nincs rendelés ezen a napon.")
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

    # elif page == "Új ügyfél regisztrálása":
    #     regisztracio.show()

# 🔥 **Fő programlogika**
if not st.session_state.authenticated:
    login_page()
else:
    main_content()
