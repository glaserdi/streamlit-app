import streamlit as st
import pandas as pd
import io
import math
import read_excel
import numpy as np
import generate_price_offer as gen_p
import datetime
import constants as C


# 🔹 TERÜLET SZÁMÍTÁS
def terulet_szamitas(hosszusag, szelesseg, darabszam, spec_forma=False, tavtarto=False):
    # Alapterület számítása
    try:
        hosszusag = float(hosszusag)
        szelesseg = float(szelesseg)
        darabszam = int(darabszam)
    except ValueError:
        return [0, 0, 0]

    if hosszusag and szelesseg:
        terulet_siman = (hosszusag * szelesseg) / 1000000  # m^2-re átváltva, ha mm-ben van megadva

        # Adalék számítása
        adalek = 0
        terulet_adalekkal = terulet_siman
        if terulet_siman <= C.MIN_TERULET or terulet_siman >= C.MAX_TERULET:
            adalek = C.ADALEK_SZORZO * terulet_siman
            terulet_adalekkal = terulet_siman + adalek  # Hozzáadjuk az adalékot az alapterülethez

        # Távtartó vagy speciális forma esetén újabb 30% adalék az aktuális területre
        if spec_forma == "Eltérő forma":
            adalek += C.FORMA_SZORZO * terulet_adalekkal
            terulet_adalekkal += C.FORMA_SZORZO * terulet_adalekkal  # Frissített terület az adalékkal

        if tavtarto == "Távtartó":
            adalek += C.TAVTARTO_ADALEK * terulet_adalekkal
            terulet_adalekkal += C.TAVTARTO_ADALEK * terulet_adalekkal

        if terulet_adalekkal >= C.MAX_TERULET:
            st.warning("⚠️ Ellenőrizd a vastagságot, biztonsági okokból!")

        # Összes terület számítása a darabszámmal
        ossz_terulet = terulet_adalekkal * darabszam

        return [round(terulet_siman, 4) * darabszam, round(adalek, 4) * darabszam, round(ossz_terulet, 2)]
    else:
        st.error("❌ Kérlek add meg a hosszúságot és a szélességet!")


@st.cache_data
def get_retegek_by_kod(termek_kod, duplex_list, triplex_list):
    if termek_kod in duplex_list:
        return "DUPLEX"
    elif termek_kod in triplex_list:
        return "TRIPLEX"


# 🔹 ÁR KALKULÁCIÓ
@st.cache_data
def get_ar(df, termek_kod, arlista_szint):
    column_name = f"Eladási Ár {arlista_szint}"
    filtered_rows = df.loc[df["Termék Kod"] == termek_kod, column_name]
    return float(filtered_rows.iloc[0]) if not filtered_rows.empty else None


def calculate_wood_pieces(df, reteg):
    lec_lista = []

    for _, row in df.iterrows():
        szelesseg = row["Szélesség"] + 20
        magassag = row["Magasság"] + 20

        lec_darabszam = 1 if reteg == "DUPLEX" else 2 if reteg == "TRIPLEX" else 1

        for _ in range(lec_darabszam):
            lec_lista.append(szelesseg)
            lec_lista.append(magassag)

    return sorted(lec_lista, reverse=True)  # Hosszabbakat először


def optimize_cutting(lec_lista, max_length=6000):
    lec_lista = sorted(lec_lista, reverse=True)  # Csökkenő sorrendben rendezzük (FFD stratégia)
    bins = []  # Tároljuk a darabolásokat
    hulladekok = []  # Tároljuk a hulladékokat

    for lec in lec_lista:
        best_fit_index = -1
        min_remaining_space = max_length + 1  # Kezdetben nagy érték

        # Próbáljuk megtalálni a legjobb helyet
        for i, bin in enumerate(bins):
            remaining_space = max_length - sum(bin)
            if remaining_space >= lec and remaining_space - lec < min_remaining_space:
                best_fit_index = i
                min_remaining_space = remaining_space - lec

        # Ha van megfelelő hely, beletesszük
        if best_fit_index != -1:
            bins[best_fit_index].append(lec)
        else:
            # Új vágást kezdünk
            bins.append([lec])

    # Hulladék számítása
    hulladekok = [max_length - sum(bin) for bin in bins]

    return bins, hulladekok


def show():
    # 🔹 EXCEL ADATOK BETÖLTÉSE (Cache-elés)
    @st.cache_data
    def load_excel_data(file_path):
        df_termek_kod = pd.read_excel(file_path, sheet_name='TermekKod')
        df_vastagsag = pd.read_excel(file_path, sheet_name='Vastagsag')
        df_cegek_arlista = pd.read_excel(file_path, sheet_name='Arlista')
        return df_termek_kod, df_vastagsag, df_cegek_arlista

    df_termek_kod, df_vastagsag, df_cegek_arlista = load_excel_data(C.FILE_PATH)

    # 🔹 TERMÉKKÓDOK LEKÉRÉSE (Cache)
    @st.cache_data
    def get_product_codes(df, reteg):
        return df[df["Reteg"] == reteg]["Termék Kod"].tolist()

    duplex_codes = get_product_codes(df_termek_kod, "Duplex")
    triplex_codes = get_product_codes(df_termek_kod, "Triplex")
    vastagsag_lista = [""] + df_vastagsag["Vastagsag"].tolist()

    # 🔹 RENDELÉSEK TÁROLÁSA
    if "adathalmaz" not in st.session_state:
        st.session_state.adathalmaz = pd.DataFrame(
            columns=["Megrendelő", "Hosszúság", "Szélesség", "Darabszám", "Terület", "Ár"])

    # 🔹 FELÜLET MEGJELENÍTÉSE
    st.title("Termó rendelések")

    bevitel = st.radio("Hogyan szeretnéd bevinni az adatokat?", ["Kézi bevitel", "Fájl feltöltése"])
    megrendelok_lista = df_cegek_arlista["Ceg neve"]

    if bevitel == "Kézi bevitel":
        megrendelo_neve = st.selectbox("Megrendelő neve:", megrendelok_lista)
        if megrendelo_neve == "Magánszemély":
            megrendelo_neve = st.text_input("Írd be a megrendelő nevét")

        tipus = st.radio("Válaszd ki a termó típusát", ["Duplex", "Triplex"])
        termek_kod = st.selectbox("Termék kód", duplex_codes if tipus == "Duplex" else triplex_codes)
        vastagsag = st.selectbox("Vastagság:", vastagsag_lista)

        st.write("**Opciók**")
        col1, col2 = st.columns(2)
        with col1:
            argon = st.checkbox("Argonnal")
            melegperem = st.checkbox("Meleg perem")
        with col2:
            tavtarto = st.checkbox("Távtartó")
            forma = st.checkbox("Eltérő forma")

        melegperem_szin = st.radio("Melegperem színe", ["Fekete", "Szürke"]) if melegperem else None

        szelesseg = st.number_input("Szélesség (mm)", min_value=1, max_value=C.MAX_MERET,
                                    placeholder="Írj be egy számot...")
        hosszusag = st.number_input("Hosszúság (mm)", min_value=1, max_value=C.MAX_MERET,
                                    placeholder="Írj be egy számot...")
        darabszam = st.number_input("Darabszám", min_value=1, value=1, placeholder="Írj be egy számot...")

        [terulet, adalek, ossz_terulet] = terulet_szamitas(hosszusag, szelesseg, darabszam, forma, tavtarto)
        st.write(f" Az üveg területe {round(terulet, 2)} m², melyhez hozzájön adalékként \
        {round(adalek, 2)} m², így az összterület = {round(terulet, 2)}  + {round(adalek, 2)} = {round(ossz_terulet, 2)} m²")

        ar = 0
        if terulet > 0:
            arlista_szint = 2 if not df_cegek_arlista.loc[
                df_cegek_arlista["Ceg neve"] == megrendelo_neve, "Arlista"].empty else 0
            eladasi_ar = get_ar(df_termek_kod, termek_kod, arlista_szint)

            if eladasi_ar:
                if melegperem_szin:
                    eladasi_ar += C.MELEGPEREM_AR.get(tipus, 0)
                ar = ossz_terulet * eladasi_ar

            ar = math.ceil(ar)
            st.write(f"💰 **Számított ár:** {ar:.2f} lej")

            if st.button("Hozzáad"):
                bevitt_adatok = {
                    "Megrendelo_neve": megrendelo_neve,
                    "Termékkód": termek_kod,
                    "Vastagság": vastagsag,
                    "Magasság": hosszusag,
                    "Szélesség": szelesseg,
                    "Terület": terulet,
                    "Adalék": adalek,
                    "Össz terület": ossz_terulet,
                    "Darabszám": darabszam,
                    "Ár": ar,
                    "Argon": argon,
                    "Távartó": tavtarto,
                    "Melegperem": melegperem_szin,
                    "Eltérő forma": forma,
                    "Üveg típusa": tipus
                }
                st.session_state.adathalmaz = pd.concat(
                    [st.session_state.adathalmaz, pd.DataFrame([bevitt_adatok])],
                    ignore_index=True
                )
                st.session_state.szelesseg = None
                st.session_state.hosszusag = None
                st.rerun()
        st.dataframe(st.session_state.adathalmaz, use_container_width=True)

        order_data_kezi = st.session_state.adathalmaz
        if not order_data_kezi.empty:
            pdf_buffer = gen_p.generate_pdf(order_data_kezi,
                                            "./logo_1.jpg",
                                            "pecset.jpg",
                                            "kezi"
                                            )

            st.download_button(
                label="📥 Letöltés PDF-ként",
                data=pdf_buffer,
                file_name=f"{megrendelo_neve}_{datetime.datetime.now()}_arajanlat.pdf",
                mime="application/pdf"
            )

        # output = io.BytesIO()
        # with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        #     st.session_state.adathalmaz.to_excel(writer, sheet_name="Rendelések", index=False)
        # output.seek(0)
        #
        # st.download_button("⬇️ Excel letöltése",
        #                    data=output,
        #                    file_name=f"rendeles_{megrendelo_neve}.xlsx",
        #                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # 🔄 CSV betöltése (ha van)
        try:
            deadlines = pd.read_csv(C.CSV_FILE)
        except FileNotFoundError:
            deadlines = pd.DataFrame(columns=["title", "start"])

        new_date = st.date_input("Határidő:", datetime.date.today())
        task_name = st.text_input("Feladat neve:")

        if st.button("Határidő hozzáadása"):
            if task_name:
                new_entry = pd.DataFrame([{"title": task_name, "start": str(new_date)}])
                deadlines = pd.concat([deadlines, new_entry], ignore_index=True)
                deadlines.to_csv(C.CSV_FILE, index=False)  # 📂 Fájlba mentés
                st.success(f"✅ Hozzáadva: {task_name} - {new_date}")
                st.rerun()
            else:
                st.warning("⚠️ Adj meg egy feladatot!")


    elif bevitel == "Fájl feltöltése":
        uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")

        if uploaded_file:
            try:
                order_data = read_excel.extract_order_data(uploaded_file)
                megrendelo_neve = order_data['Megrendelő_neve'].iloc[0]
                hatarido = str(order_data['Határidő'].iloc[0]).split(" ")[0]
                sorszam = order_data['Sorszám_Megrendelés'].iloc[0]
                arlista_szint = 2 if not df_cegek_arlista.loc[
                    df_cegek_arlista["Ceg neve"] == megrendelo_neve, "Arlista"].empty else 0
                order_data["Megrendelo_neve"] = megrendelo_neve
                required_columns = ["Szélesség", "Magasság", "Üveg típusa"]
                if all(col in order_data.columns for col in required_columns):

                    order_data['Terület'] = order_data.apply(
                        lambda row: terulet_szamitas(row['Magasság'],
                                                     row['Szélesség'],
                                                     row['Darabszám'],
                                                     row["Eltérő forma"],
                                                     row["Távtartó"]
                                                     )[0], axis=1)
                    order_data['Adalék'] = order_data.apply(
                        lambda row: terulet_szamitas(row['Magasság'],
                                                     row['Szélesség'],
                                                     row['Darabszám'],
                                                     row["Eltérő forma"],
                                                     row["Távtartó"]
                                                     )[1], axis=1)
                    order_data['Össz terület'] = order_data.apply(
                        lambda row: terulet_szamitas(row['Magasság'],
                                                     row['Szélesség'],
                                                     row['Darabszám'],
                                                     row["Eltérő forma"],
                                                     row["Távtartó"]
                                                     )[2], axis=1)

                    order_data["Egységár"] = order_data.apply(
                        lambda row: get_ar(df_termek_kod, row["Üveg típusa"], arlista_szint), axis=1
                    )

                    if order_data["Melegperem"][0] == "fekete" or order_data["Melegperem"][0] == "szürke":
                        order_data["Egységár"] = order_data["Egységár"] + 35

                    order_data["Ár"] = order_data.apply(
                        lambda row: row["Egységár"] * row['Össz terület'], axis=1
                    )

                    order_data["Ár"] = order_data["Ár"].apply(np.ceil)
                    st.dataframe(order_data[
                                     ["Szélesség", "Magasság", "Darabszám", "Üveg vastagsága", "Melegperem", "Terület",
                                      "Adalék", "Üveg típusa", "Össz terület", "Ár"]])

                    st.write(f"💰 **Számított ár:** {order_data["Ár"].sum()} lej")
                else:
                    missing_cols = [col for col in required_columns if col not in order_data.columns]
                    st.error(f"❌ Hiányzó oszlopok: {', '.join(missing_cols)}")
            except Exception as e:
                st.error(f"Hiba történt a fájl feldolgozása közben: {e}")

            arlista_szint = 2 if not df_cegek_arlista.loc[
                df_cegek_arlista["Ceg neve"] == megrendelo_neve, "Arlista"].empty else 0

            order_data["Egységár"] = order_data.apply(
                lambda row: get_ar(df_termek_kod, row["Üveg típusa"], arlista_szint),
                axis=1
            )

            pdf_buffer = gen_p.generate_pdf(order_data, "./logo_1.jpg", "pecset.jpg", "file")

            st.download_button(
                label="📥 Letöltés PDF-ként",
                data=pdf_buffer,
                file_name=f"{megrendelo_neve}_{datetime.datetime.now()}_arajanlat.pdf",
                mime="application/pdf"
            )

            if st.button("✅ Árajánlat elfogadása"):
                try:
                    deadlines = pd.read_csv(C.CSV_FILE)
                except FileNotFoundError:
                    deadlines = pd.DataFrame(columns=["title", "start"])

                new_entry = pd.DataFrame([{"title": f"{megrendelo_neve} {sorszam}", "start": f"{hatarido}"}])
                deadlines = pd.concat([deadlines, new_entry], ignore_index=True)
                deadlines.to_csv(C.CSV_FILE, index=False)  # 📂 Fájlba mentés

            st.title("Optimalizált lécvágási Kalkulátor")

            # lec méretek számítása
            lec_lista = calculate_wood_pieces(order_data,
                                              get_retegek_by_kod(order_data.iloc[0]["Üveg típusa"], duplex_codes,
                                                                 triplex_codes))
            st.dataframe(order_data)
            st.write(order_data.iloc[0]["Üveg típusa"])

            # Optimalizált vágási terv kiszámítása
            cutting_plan, hulladekok = optimize_cutting(lec_lista, 6000)

            # Összes hulladék kiszámítása
            osszes_hulladek_mm = sum(hulladekok)
            osszes_hulladek_cm = osszes_hulladek_mm / 10

            # Eredmények megjelenítése
            st.subheader("Optimalizált Vágási Terv")
            for i, batch in enumerate(cutting_plan):
                st.write(f"**{i + 1}. lec (6m)**: {batch} mm")
                st.write(f"➡️ Felhasznált hossz: {sum(batch)} mm | Hulladék: {hulladekok[i]} mm")

            st.subheader("Összegzés")
            st.write(f"**Felhasznált lecek száma:** {len(cutting_plan)} db")
            st.write(f"**Összes hulladék:** {osszes_hulladek_mm} mm ({osszes_hulladek_cm:.2f} cm)")
            st.write(f"**Hulladék hosszok mm-ben:** {hulladekok}")

            # Letölthető vágási terv
            cutting_df = pd.DataFrame({
                "lec sorszám": list(range(1, len(cutting_plan) + 1)),
                "Vágott méretek": [str(batch) for batch in cutting_plan],
                "Hulladék (mm)": hulladekok
            })

            csv = cutting_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Vágási terv letöltése CSV formátumban",
                data=csv,
                file_name="lec_vagasi_terv.csv",
                mime="text/csv",
            )
