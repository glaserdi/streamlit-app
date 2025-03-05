import streamlit as st
import pandas as pd
import constants as C
import datetime
import numpy as np
import math
import read_excel

lyukak_ara = []
csiszolas_ara = 0
ar = 0
def load_excel_data(file_path):
    df_vagott_uveg_kod = pd.read_excel(file_path, sheet_name='Vagott uvegek')
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


def calculate_price(row, arlista_szint):
    terulet = row['Magasság'] * row['Szélesség']
    vastagsag = row["Üveg típusa"].split()[-1][:-2]
    eladasi_ar = get_ar(df_vagott_uveg_kod, row['Üveg típusa'], arlista_szint)
    ar = np.ceil(row["Terület"] * eladasi_ar)

    szelesseg_count = row["Csiszolás"].count("Szélesség")
    magassag_count = row["Csiszolás"].count("Magasság")
    csiszolas_ara = C.csiszolas_arak[str(vastagsag)]

    ar += math.ceil(
        ((szelesseg_count * row["Szélesség"]) + (magassag_count * row["Magasság"])) / 1000 * csiszolas_ara
    )*row["Darabszám"]

    return ar

def show(user_role, user_name):

    st.title("🪞 Vágott üveg rendelések")

    bevitel = st.radio("Hogyan szeretnéd bevinni az adatokat?", ["Kézi bevitel", "Fájl feltöltése"])
    megrendelok_lista = df_cegek_arlista["Ceg neve"]

    if bevitel == "Kézi bevitel":
        megrendelo_neve = user_name if user_role == "vasarlo" else st.selectbox("Megrendelő neve:", megrendelok_lista)
        if megrendelo_neve == "Magánszemély":
            megrendelo_neve = st.text_input("Írd be a megrendelő nevét")

        rendeles_sorszama = st.number_input("Rendelés sorszáma", step=1)
        hatarido = st.date_input("Kérlek add meg az elkészítés határidejét:", datetime.date.today())
        vastagsag = st.selectbox("Üveg vastagsága", [2, 3, 4, 6, 8])
        szurt_termekek = df_vagott_uveg_kod[df_vagott_uveg_kod["Termék Kod"].str.contains(f"{vastagsag}mm", na=False)]
        tipus = st.selectbox("Válaszd ki az üveg kódját", szurt_termekek)

        st.write("**Opciók**")

        csiszolas = st.checkbox("Csiszolás géppel")
        if csiszolas:
            csiszolas = "csiszolás"

        csiszolas_kezi = st.checkbox("Csiszolás kézzel")
        if csiszolas_kezi:
            csiszolas = "csiszolás kézi"

        if csiszolas == "csiszolás" or csiszolas == "csiszolás kézi":
            oldalak_szama = st.selectbox("Hány oldalát kell csiszolni?", [1, 2, 3, 4])
            if oldalak_szama == 1:
                csiszolando_oldal = st.selectbox("Melyik oldalt kell csiszolni?", ["Szélesség", "Magasság"])
            elif oldalak_szama == 2:
                csiszolando_oldal = st.selectbox("Melyik oldalakat kell csiszolni?",
                                                 ["Szélesség + Szélesség", "Szélesség + Magasság", "Magasság + Magasság"])
            elif oldalak_szama == 3:
                csiszolando_oldal = st.selectbox("Melyik oldalakat kell csiszolni?",
                                                 ["Szélesség + Magasság + Magasság", "Magasság + Szélesség + Szélesség"])
            elif oldalak_szama == 4:
                csiszolando_oldal = "Szélesség + Magasság + Magasság + Szélesség"

        lyuk = st.checkbox("Lyukfúrás")

        lyuk_meretek = []
        if lyuk:
            lyuk_5_6 = st.number_input("Hány db 5-6mm átmérőjű lyukat szeretnél?", min_value=0, step=1, value=0)
            lyuk_8_26 = st.number_input("Hány db 8-26mm átmérőjű lyukat szeretnél?", min_value=0, step=1, value=0)
            lyuk_30_55 = st.number_input("Hány db 30-55mm átmérőjű lyukat szeretnél?", min_value=0, step=1, value=0)

            # Listák a méretek és árak tárolására
            lyuk_meretek = []
            lyukak_ara = []

            # Ha a felhasználó beírt darabszámokat, számoljuk ki az árat
            if lyuk_5_6 > 0:
                lyuk_meretek.extend(["5-6"] * lyuk_5_6)
                lyukak_ara.append(lyuk_5_6 * lyuk_egyseg_ar("5-6"))

            if lyuk_8_26 > 0:
                lyuk_meretek.extend(["8-26"] * lyuk_8_26)
                lyukak_ara.append(lyuk_8_26 * lyuk_egyseg_ar("8-26"))

            if lyuk_30_55 > 0:
                lyuk_meretek.extend(["30-55"] * lyuk_30_55)
                lyukak_ara.append(lyuk_30_55 * lyuk_egyseg_ar("30-55"))

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
        if csiszolas == "csiszolás kézi":
            csiszolas_ara = C.csiszolas_arak.get("kezi")
        elif csiszolas == "csiszolás":
            csiszolas_ara = C.csiszolas_arak[str(vastagsag)]

        if csiszolas:
            oldalak_lista = csiszolando_oldal.split(" + ")

            # Számláljuk az egyes oldalak előfordulásait
            szelesseg_count = oldalak_lista.count("Szélesség")
            magassag_count = oldalak_lista.count("Magasság")

            szelesseg = szelesseg if szelesseg is not None else 0
            magassag = magassag if magassag is not None else 0
            csiszolas_ara = csiszolas_ara if csiszolas_ara is not None else 1

            ar += math.ceil(((szelesseg_count * szelesseg) + (magassag_count * magassag))/1000 * csiszolas_ara)

        szereles = st.selectbox("Szerelés típusa", ["Szerelés nélkül",
                                                    "Szerelés saját műhelyünkben",
                                                    "Szerelés helyszínen",
                                                    "Munkagép ragasztva",
                                                    "Munkagép szereléssel"])
        if szereles == "Szerelés saját műhelyünkben":
            ar += ar * C.szereles_sajat_muhely
        elif szereles == "Szerelés helyszínen":
            ar += ar * C.szereles_helyszinen
        elif szereles == "Munkagép ragasztva":
            ar += ar * C.szereles_munkagep_ragasztva
        elif szereles == "Munkagép szereléssel":
            ar += ar * C.szereles_munkagep

        ar = ar * darabszam
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
                order_data_file = read_excel.extract_order_data_vagott_uveg(uploaded_file)
                megrendelo_neve = order_data_file['Megrendelő_neve'].iloc[0]
                hatarido = str(order_data_file['Határidő'].iloc[0]).split(" ")[0]
                sorszam = order_data_file['Sorszám_Megrendelés'].iloc[0]
                arlista_szint = 2 if not df_cegek_arlista.loc[
                    df_cegek_arlista["Ceg neve"] == megrendelo_neve, "Arlista"].empty else 0
                order_data_file["Megrendelo_neve"] = megrendelo_neve
                required_columns = ["Szélesség", "Magasság", "Üveg típusa"]
                if all(col in order_data_file.columns for col in required_columns):
                    order_data_file['Terület'] = order_data_file.apply(
                        lambda row: (row["Magasság"] * row["Szélesség"] * row["Darabszám"])/1000000, axis=1)
                    order_data_file["Ár"] = order_data_file.apply(lambda row: calculate_price(row, arlista_szint), axis=1)

                    st.dataframe(order_data_file[
                                     ["Szélesség", "Magasság", "Darabszám", "Terület",
                                       "Üveg típusa", "Csiszolás", "Ár"]], hide_index=True, use_container_width=True)

                    st.write(f"💰 **Számított ár:** {np.ceil(order_data_file["Ár"].sum())} lej")

            except Exception as e:
                st.error(f"Hiba történt a fájl feldolgozása közben: {e}")






