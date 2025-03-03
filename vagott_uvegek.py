import streamlit as st
import pandas as pd
import constants as C
import datetime
import numpy as np

lyukak_ara = []
csiszolas_ara = 0
ar = 0
def load_excel_data(file_path):
    df_vagott_uveg_kod = pd.read_excel(file_path, sheet_name='EgyediTermekKod')
    df_cegek_arlista = pd.read_excel(file_path, sheet_name='Arlista')
    return df_vagott_uveg_kod, df_cegek_arlista

df_vagott_uveg_kod,df_cegek_arlista = load_excel_data(C.FILE_PATH)

if "adathalmaz" not in st.session_state:
    st.session_state.adathalmaz = pd.DataFrame()

def lyuk_egyseg_ar(atmero):
    for key, value in C.lyuk_arak.items():
        if key == atmero:
            return value
@st.cache_data
def get_ar(df, termek_kod, arlista_szint):
    column_name = f"Eladási Ár {arlista_szint}"
    filtered_rows = df.loc[df["Termék Kod"] == termek_kod, column_name]
    return float(filtered_rows.iloc[0]) if not filtered_rows.empty else None


def show(user_role: str, user_name:str):
    st.title("🪞 Vágott üveg rendelések")
    
    bevitel = st.radio("Hogyan szeretnéd bevinni az adatokat?", ["Kézi bevitel", "Fájl feltöltése"])
    megrendelok_lista = df_cegek_arlista["Ceg neve"]

    if bevitel == "Kézi bevitel":
        megrendelo_neve = user_name if user_role == "vasarlo" else st.selectbox("Megrendelő neve:", megrendelok_lista)
        if megrendelo_neve == "Magánszemély":
            megrendelo_neve = st.text_input("Írd be a megrendelő nevét")

        rendeles_sorszama = st.number_input("Rendelés sorszáma", step=1)
        hatarido = st.date_input("Kérlek add meg az elkészítés határidejét:", datetime.date.today())
        tipus = st.selectbox("Válaszd ki az üveg kódját", df_vagott_uveg_kod["Termék Kod"])

        st.write("**Opciók**")
        csiszolas = st.checkbox("Csiszolás")
        lyuk = st.checkbox("Lyukfúrás")

        lyuk_meretek = []
        if lyuk:
            lyuk_szam = st.number_input("Hány lyuk átmérőjét szeretnéd kiválasztani?", min_value=1, step=1, value=1)
            for i in range(lyuk_szam):
                meret = st.selectbox(f"Válaszd ki a {i + 1}. lyuk átmérőjét:", ["5-6", "7-25", "26-55"],
                                     key=f"lyuk_{i}")
                lyuk_meretek.append(meret)
                lyukak_ara.append(lyuk_egyseg_ar(meret))

        szelesseg = st.number_input("Szélesség (mm)", min_value=1, max_value=C.MAX_MERET,
                                    placeholder="Írj be egy számot...")
        magassag = st.number_input("Magasság (mm)", min_value=1, max_value=C.MAX_MERET,
                                   placeholder="Írj be egy számot...")
        darabszam = st.number_input("Darabszám", min_value=1, value=1, placeholder="Írj be egy számot...")

        terulet = (szelesseg * magassag) / 1000000
        kerulet = 2 * (szelesseg + magassag) / 1000

        arlista_szint = 2 if not df_cegek_arlista.loc[
            df_cegek_arlista["Ceg neve"] == megrendelo_neve, "Arlista"].empty else 0
        eladasi_ar = get_ar(df_vagott_uveg_kod, tipus, arlista_szint)

        ar = np.ceil(terulet * eladasi_ar)
        if lyuk:
            ar += sum(lyukak_ara)
        if csiszolas:
            csiszolas_ara = 25
            ar += np.ceil(kerulet * csiszolas_ara)

        st.write(f"Számított ár: {ar} RON")

        if st.button("Hozzáad"):
            uj_sorszam = 1 if st.session_state.adathalmaz.empty else int(
                st.session_state.adathalmaz["Sorszám"].max()) + 1

            bevitt_adatok = {
                "Sorszám": uj_sorszam,
                "Megrendelo_neve": megrendelo_neve,
                "Magasság": magassag,
                "Szélesség": szelesseg,
                "Terület": terulet,
                "Kerület": kerulet,
                "Darabszám": darabszam,
                "Ár": ar*darabszam,
                "Üveg típusa": tipus,
                "Határidő": hatarido,
                "Rendelés sorszáma": rendeles_sorszama
            }

            st.session_state.adathalmaz = pd.concat(
                [st.session_state.adathalmaz, pd.DataFrame([bevitt_adatok])],
                ignore_index=True
            )

            # **Árak és listák alaphelyzetbe állítása**
            lyukak_ara.clear()
            csiszolas_ara = 0
            ar = 0

            st.rerun()

        else:
            st.warning("Kérlek, töltsd ki a kötelező mezőket!")

        # # Adattábla megjelenítése
        if not st.session_state.adathalmaz.empty:
            st.dataframe(st.session_state.adathalmaz, hide_index=True) #[[
        #         "Sorszám", "Termékkód", "Szélesség", "Magasság", "Darabszám", "Üveg vastagsága",
        #         "Melegperem", "Távtartó", "Eltérő forma", "Terület", "Adalék", "Össz terület", "Ár"
        #     ]], use_container_width=True, hide_index=True)
        #
            # Sor törlése
            st.session_state.adathalmaz["Sorszám"] = st.session_state.adathalmaz["Sorszám"].astype(int)
            sorszamok = st.session_state.adathalmaz["Sorszám"].tolist()
            st.header("Elrontottad? Töröld ki ✏️")

            sorszam_to_delete = st.selectbox("Válassz sorszámot törléshez:", sorszamok)

            if st.button("Sor törlése"):
                st.session_state.adathalmaz = st.session_state.adathalmaz[
                    st.session_state.adathalmaz["Sorszám"] != sorszam_to_delete
                    ].reset_index(drop=True)
                st.success(f"A(z) {sorszam_to_delete}. sor törölve!")
                st.rerun()
        else:
            st.warning("Nincs adat a táblázatban!")


        order_data_kezi = st.session_state.adathalmaz
        # if not order_data_kezi.empty:
        #     pdf_buffer = gen_p.generate_pdf(order_data_kezi,
        #                                     "./logo_1.jpg",
        #                                     "pecset.jpg",
        #                                     "kezi",
        #                                     rendeles_sorszama
        #                                     )
        #     gyartas_pdf_buffer = gen_p.generate_gyartasi_pdf(order_data_kezi, "kezi", rendeles_sorszama, hatarido)
        #
        #     st.header("Árajánlat generálása 🧮")
        #     st.download_button(
        #         label="📥 Letöltés PDF-ként",
        #         data=pdf_buffer,
        #         file_name=f"{megrendelo_neve}_{datetime.datetime.now()}_arajanlat.pdf",
        #         mime="application/pdf"
        #     )
        #
        #     if user_role != "vasarlo":
        #         st.header("Gyártási adatok generálása 💡")
        #         st.download_button(
        #             label="📥 Letöltés PDF-ként",
        #             data=gyartas_pdf_buffer,
        #             file_name=f"{megrendelo_neve}_{datetime.datetime.now()}_gyartas.pdf",
        #             mime="application/pdf"
        #         )
        #
        #     st.header("Rendelés leadása 🛒")
        #     elfogadas = st.checkbox("Árajánlat elfogadása")
        #
        #     task_name = f"{order_data_kezi["Megrendelo_neve"].iloc[0]} {round(rendeles_sorszama)}"
        #     if elfogadas:
        #         if user_role == "vasarlo":
        #             st.title("Árajánlat ellenőrzésre küldése e-mailben")
        #             # Checkbox az e-mail küldéshez
        #             if st.checkbox("Feltöltöm ellenőrzésre e-mailben"):
        #                 result = send_email(pdf_buffer.getvalue(),
        #                                     order_data_kezi,
        #                                     rendeles_sorszama, hatarido,
        #                                     st.session_state.username)  # Kiolvassuk a tartalmat bájtokként
        #                 if "Sikeresen" in result:
        #                     st.success(result)
        #                 else:
        #                     st.error(result)
        #      #st.rerun()
        #         else:
        #             st.warning("⚠️ Adj meg egy feladatot!")
        #     if user_role == "vasarlo":
        #         st.error(f"FIGYELEM!!! A rendelés véglegesítéséhez egy alkalmazottunk átnézi a rendelésed.")
    if bevitel == "Fájl feltöltése":
        uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")

        if uploaded_file:
            try:
                pass
            except Exception as e:
                st.error(f"Hiba történt a fájl feldolgozása közben: {e}")


