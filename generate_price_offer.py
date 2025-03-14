from fpdf import FPDF
from datetime import datetime
import io
import numpy as np
def generate_pdf(order_data, company_logo_path, pecset_path , bevitel=None, sorszam=None):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    start_x = 10  # Táblázat kezdőindex
    # Cég logó bal felső sarokban
    pdf.image(company_logo_path, x=10, y=8, w=40)

    # 🔹 Cég elérhetőségek a jobb felső sarokba
    pdf.set_font("Arial", "", 10)
    pdf.set_xy(140, 10)  # Jobb felső sarokba igazítás
    pdf.multi_cell(60, 5,
                   "Telefon: +40 740 169 912\nEmail: glaserdiuvegezo@gmail.com\n Cím: Gyergyószentmiklós, \n Kossuth Lajos utca, 233",
                   align="R")

    # Árajánlat cím és dátum középen
    pdf.set_xy(10, 15)  # Új pozíció beállítása a következő tartalomhoz
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ÁRAJÁNLAT", ln=1, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Dátum: {datetime.now().strftime('%Y-%m-%d')}", ln=0.1, align="C")
    pdf.cell(0, 4, f"Ajánlatot kérte: {order_data['Megrendelo_neve'].iloc[0]}", ln=0.1, align="C")
    if bevitel == "file":
        pdf.cell(0, 10,f"Sorszám: {order_data['Sorszám_Megrendelés'].iloc[0]}", ln=0.1, align="C")
    else:
        pdf.cell(0, 4, f"Sorszám: {sorszam}", ln=0.1, align="C")
    pdf.ln(5)  # Távolság a táblázat előtt

    # 🔹 Táblázat fejléc
    pdf.set_font("Arial", "B", 10.5)
    column_widths = [45, 20, 20, 20, 10, 20, 15, 22, 22]
    headers = ["Üveg típusa", "Extrák", "Szélesség", "Magasság", "Db", "Terület", "Adalék", "Összterület", "Ár"]

    pdf.set_x(start_x)
    for i, header in enumerate(headers):
        pdf.cell(column_widths[i], 10, header, 1, align="C")
    pdf.ln()

    # 🔹 Táblázat adatok
    pdf.set_font("Arial", "", 10)
    total_price = 0
    total_area = 0
    ossz_adalek = 0
    ossz_darabszam = 0
    ossz_sima_terulet = 0

    if bevitel == "kezi":
        order_data["Üveg típusa"] = order_data["Termékkód"]
    for _, row in order_data.iterrows():
        extrak = ""
        if "Melegperem" in row:
            if row["Melegperem"] == "szürke" or "fekete":
                extrak += " MP"
        if "Távtartó" in row:
            if row["Távtartó"] == "Távtartó":
                extrak += " TT"
        if "Eltérő forma" in row:
            if row["Eltérő forma"] == "Eltérő forma":
                extrak += " EF"

        col_data = [
            str(row["Üveg típusa"]),
            str(extrak),
            str(round(row["Szélesség"])),
            str(round(row["Magasság"])),
            str(round(row["Darabszám"])),
            f"{row['Terület']:.2f}",
            f"{row['Adalék']:.2f}",
            f"{row['Összterület']:.2f}",
            f"{row['Ár']:.2f}"
        ]

        # 🔹 Az "Üveg típusa" cella több sort is elfoglalhat, ezért kiszámítjuk a magasságát
        start_x = pdf.get_x()
        start_y = pdf.get_y()

        pdf.set_x(start_x)
        pdf.multi_cell(column_widths[0], 6, col_data[0], border=1, align="C")
        end_y = pdf.get_y()  # Multi-cell utáni Y pozíció

        row_height = end_y - start_y  # A multi-cell által használt teljes magasság

        # Ha a row_height túl alacsony lenne, állítsunk be egy minimum magasságot
        row_height = max(row_height, 6)

        pdf.set_xy(start_x + column_widths[0], start_y)  # A következő cella kezdőpozíciója

        for i in range(1, len(col_data)):
            pdf.cell(column_widths[i], row_height, col_data[i], border=1, align="C")

        pdf.ln(row_height)  # Következő sorra ugrás

        ossz_sima_terulet += row["Terület"]
        ossz_darabszam += row["Darabszám"]
        total_area += row["Összterület"]
        total_price += row["Ár"]
        ossz_adalek += row["Adalék"]


    # 🔹 Összegzés sor igazítása a megfelelő oszlopok alá
    pdf.set_x(start_x)
    pdf.set_font("Arial", "B", 11)

    pdf.cell(sum(column_widths[:4]), 10, "Összesen:", 1,
             align="C")  # Az első három oszlop (szélesség, magasság, üveg típusa) összevonva
    #pdf.cell(column_widths[5], 10, "", 1)  # Üres cella az "Összterület" alatt
    pdf.cell(column_widths[4], 10, f"{round(ossz_darabszam)}",1, align="C")
    pdf.cell(column_widths[5], 10, f"{ossz_sima_terulet:.2f} m²",1, align="C")
    pdf.cell(column_widths[6], 10, f"{ossz_adalek:.2f} m²", 1, align="C")  # Adalék alatt
    pdf.cell(column_widths[7], 10, f"{total_area:.2f} m²", 1, align="C")
    pdf.cell(column_widths[8], 10, f"{int(np. ceil(total_price))} lei", 1, align="C")  # Összesített ár

    # 🔹 Aláírás és pecsét elhelyezése
    # 🔹 Megjegyzések szekció
    pdf.ln(20)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 10, "Megjegyzések:", ln=1)

    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 4, "A kis terület adalék +20%, ha a terület kisebb mint 0.3 m².", ln=1)
    pdf.cell(0, 4, "Extra méret adalék +20%, ha a terület nagyobb mint 2.5 m².", ln=1)
    pdf.cell(0, 4, "MP = Meleg peremmel", ln=1)
    pdf.cell(0, 4, "TT = Távtartóval", ln=1)
    pdf.cell(0, 4, "EF = Eltérõ forma", ln=1)

    pdf.ln(20)  # Távolság az aláírások előtt

    # 🔹 Két oszlop az aláírásoknak
    x_left = 30  # Bal oldal: Cég munkatársa
    x_right = 130  # Jobb oldal: Ügyfél aláírása

    pdf.set_font("Arial", "B", 11)

    # 🔹 "Cég munkatársa"
    pdf.set_xy(x_left, pdf.get_y())
    pdf.cell(60, 5, "Cég munkatársa", ln=1, align="L")

    # 🔹 "Ügyfél aláírása"
    pdf.set_xy(x_right, pdf.get_y() - 5)
    pdf.cell(60, 5, "Ügyfél aláírása", ln=1, align="L")

    # 🔹 Aláírási vonalak
    pdf.set_xy(x_left, pdf.get_y() + 15)
    pdf.cell(60, 0, "_________________", ln=1, align="L")

    pdf.set_xy(x_right, pdf.get_y())
    pdf.cell(60, 0, "_________________", ln=1, align="L")

    # 🔹 Pecsét az aláírások alatt, középen
    pdf.ln(15)  # Távolság az aláírások után
    pdf.set_x((210 - 150) / 2)  # Középre igazítás
    pdf.image(pecset_path, w=30)  # Pecsét beillesztése

    # 🔹 Mentés
    buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_output)
    buffer.seek(0)
    return buffer

def generate_gyartasi_pdf(order_data, bevitel=None, sorszam=None, hatarido=None):
        # Oszlopnevek tisztítása (felesleges szóközök eltávolítása)
    order_data.columns = order_data.columns.str.strip()
    
    # Ha fájl alapján dolgozunk
    if bevitel == "file":
        expected_columns = ["Sorszám Megrendelés", "Megrendelo_neve", "Termékkód", "Szélesség", "Magasság", "Darabszám", "Terület", "Adalék", "Összterület", "Ár"]
        rename_map = {
            "Sorszám Megrendelés": "Sorszám",
            "Termékkód": "Üveg típusa",
            "Összterület": "Összterület"
        }
    
    # Ha kézi bevitel alapján dolgozunk
    elif bevitel == "kezi":
        expected_columns = ["Sorszám", "Megrendelo_neve", "Üveg típusa", "Szélesség", "Magasság", "Darabszám", "Terület", "Adalék", "Összterület", "Ár"]
        rename_map = {}
    
    # Átnevezés, ha szükséges
    order_data.rename(columns=rename_map, inplace=True)
    
    # Ellenőrizzük, hogy minden szükséges oszlop benne van-e a DataFrame-ben
    missing_columns = [col for col in expected_columns if col not in order_data.columns]
    if missing_columns:
        print(f"Hiányzó oszlopok: {missing_columns}")

    
    order_data["Kerület"] = 2 * (order_data["Szélesség"] + order_data["Magasság"]) * order_data["Darabszám"]
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    def create_table(headers, column_widths, data, second=None):
        pdf.set_font("Arial", "B", 11)
        if second:
            pdf.ln(25)
        pdf.cell(0, 10, f"Megrendelõ: {order_data['Megrendelo_neve'].iloc[0]} \t\t\t\t\tSorszám: {sorszam} \t\t\t\t\tHatáridõ: {hatarido}", ln=1, align="C")
        pdf.ln(5)

        pdf.set_font("Arial", "B", 10.5)
        for i, header in enumerate(headers):
            pdf.cell(column_widths[i], 10, header, 1, align="C")
        pdf.ln()
        pdf.set_font("Arial", "", 10)

        for row in data:
            start_x = pdf.get_x()
            start_y = pdf.get_y()

            try:
                terulet = float(row[5]) if row[5] else 0
                darabszam = float(row[4]) if row[4] else 1
            except ValueError:
                terulet, darabszam = 0, 1

            # Piros szöveg CSAK az első táblázatban
            if second is None and "6" not in row[1]:
                if darabszam > 0 and (terulet / darabszam) >= 2.5:
                    pdf.set_text_color(255, 0, 0)
                    pdf.set_font("Arial", "B", 10)
                else:
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", "", 10)

            pdf.multi_cell(column_widths[0], 6, row[0], border=1, align="C")
            end_y = pdf.get_y()
            row_height = max(6, end_y - start_y)
            pdf.set_xy(start_x + column_widths[0], start_y)
            for i in range(1, len(row)):
                pdf.cell(column_widths[i], row_height, row[i], border=1, align="C")
            pdf.ln(row_height)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 10)
        pdf.cell(sum(column_widths[:4]), 10, "Összesen:", 1, align="C")
        pdf.cell(column_widths[4], 10, f"{round(sum(order_data['Darabszám']))}", 1, align="C")
        if second:
            pdf.cell(column_widths[5], 10, f"{round((sum(order_data['Kerület'])/1000), 2)} m", 1, align="C")
            pdf.cell(column_widths[6], 10, "", 1, align="C")
            pdf.cell(column_widths[7], 10, "", 1, align="C")
        else:
            pdf.cell(column_widths[5], 10, f"{round(sum(order_data['Terület']), 2)} m²", 1, align="C")
            pdf.cell(column_widths[6], 10, "", 1, align="C")

    # Oszlopnevek tisztítása
    order_data = order_data.rename(columns=lambda x: x.strip().replace(" ", "_"))

    # Első táblázat
    headers1 = ["Sorszám", "Üveg típusa", "Szélesség", "Magasság", "Db", "Terület", "Extrák"]
    column_widths1 = [20, 55, 20, 20, 15, 25, 25]
    data1 = []
    
    for index, row_tuple in enumerate(order_data.sort_values(by="Üveg_típusa").itertuples(), start=1):
        row = row_tuple._asdict()
        extrak = "".join([
            " MP" if row.get("Melegperem") in ["szürke", "fekete", "Szürke", "Fekete"] else "",
            " TT" if row.get("Távtartó") == "Távtartó" else "",
            " EF" if row.get("Eltérő_forma") == "Eltérő_forma" else "",
            " AR" if row.get("Argon") == "Argon" else ""
        ])
        data1.append([
            str(index), str(row["Üveg_típusa"]),
            str(round(row["Szélesség"])),
            str(round(row["Magasság"])),
            str(round(row["Darabszám"])),
            str(round(row["Terület"], 2)),
            extrak
        ])
    
    create_table(headers1, column_widths1, data1)

    # Második táblázat
    headers2 = ["Sorszám", "Üveg típusa", "Szélesség", "Magasság", "Db", "Kerület", "Extrák", "Vastagság"]
    column_widths2 = [15, 55, 20, 20, 10, 20, 30, 20]
    data2 = []

    for index, row_tuple in enumerate(order_data.sort_values(by="Üveg_típusa").itertuples(), start=1):
        row = row_tuple._asdict()
        extrak = "".join([
            " SzMP" if row.get("Melegperem") in ["szürke", "Szürke"] else "",
            " FMP" if row.get("Melegperem") in ["fekete", "Fekete"] else "",
            " TT" if row.get("Távtartó") == "Távtartó" else "",
            " EF" if row.get("Eltérő_forma") == "Eltérő_forma" else "",
            " AR" if row.get("Argon") == "Argon" else ""
        ])
        data2.append([
            str(index), str(row["Üveg_típusa"]),
            str(round(row["Szélesség"]/10, 1)),
            str(round(row["Magasság"]/10, 1)),
            str(round(row["Darabszám"])),
            str(round(row["Kerület"]/1000, 2)),
            extrak,
            str(int(row["Üveg_vastagsága"]))
        ])

    create_table(headers2, column_widths2, data2, second=True)

    # PDF létrehozása
    pdf_output = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_output)
    buffer.seek(0)
    return buffer

