import streamlit as st
import rendelesek
import termok
import vagott_uvegek
import pandas as pd
from streamlit_calendar import calendar
import tusolofulkek
import kepkeretek
import toml


st.set_page_config(layout="wide")

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
            events = [{"title": row["title"], "start": row["start"].strftime("%Y-%m-%d")} for _, row in
                      df.iterrows()]

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

        st.header("✏️ Határidő Módosítása")
        if not deadlines.empty:
            selected_deadline = st.selectbox("Válassz egy határidőt módosításra:", deadlines["title"])

            # 🔹 Az aktuális dátum kinyerése a kiválasztott cím alapján
            current_date = deadlines.loc[deadlines["title"] == selected_deadline, "start"].values[0]

            # 🔹 Módosítási lehetőségek
            new_date = st.date_input("Új határidő:", pd.to_datetime(current_date))
            new_title = st.text_input("Új név:", selected_deadline, key="new_title")

            if st.button("Módosítás mentése"):
                # 🔹 Az adott határidő módosítása
                deadlines.loc[deadlines["title"] == selected_deadline, ["title", "start"]] = [new_title,
                                                                                              new_date.strftime(
                                                                                                  "%Y-%m-%d")]

                # 🔹 Módosított fájl mentése
                deadlines.to_csv(file_path, index=False)
                st.success(f"✅ '{selected_deadline}' módosítva '{new_title}' névre és új dátuma: {new_date.strftime('%Y-%m-%d')}!")
                st.rerun()

        st.header("🗑️  Határidő törlése")
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


    # # 🔹 Összes határidő törlése
    #
    # if not deadlines.empty and st.button("Összes határidő törlése"):
    #     deadlines = pd.DataFrame(columns=["title", "start"])
    #     deadlines.to_csv(file_path, index=False)
    #     st.warning("🗑️ Minden határidő törölve!")
    #     st.rerun()

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

    # if st.button("Kijelentkezés"):
    #     st.session_state.authenticated = False
    #     st.session_state.role = None
    #     st.session_state.username = None
    #     st.rerun()

# 🔥 **Fő programlogika**
if not st.session_state.authenticated:
    login_page()
else:
    main_content()
