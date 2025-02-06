import streamlit as st
import pandas as pd
import datetime
from streamlit_calendar import calendar
def show():
    st.balloons()

    # st.title("📆 Határidő Naptár")
    #
    # # Fájl betöltése
    # file_path = "./deadlines.csv"
    # try:
    #     df = pd.read_csv(file_path)
    #     df["start"] = pd.to_datetime(df["start"], errors="coerce")
    #
    #     # Ellenőrizzük, hogy nincs-e rossz dátum
    #     df = df.dropna(subset=["start"])
    #
    #     # Streamlit Calendar események létrehozása
    #     events = [{"title": row["title"], "start": row["start"].strftime("%Y-%m-%d")} for _, row in df.iterrows()]
    #
    #     # Naptár megjelenítése
    #     calendar(events)
    #
    # except Exception as e:
    #     st.error(f"Hiba történt az adatok beolvasása közben: {e}")
    #
    #
    # # 🗑️ **Határidők törlése**
    # if st.button("Összes határidő törlése"):
    #     deadlines = pd.DataFrame(columns=["title", "start"])
    #     deadlines.to_csv(file_path, index=False)
    #     st.warning("🗑️ Minden határidő törölve!")
    #     st.rerun()

