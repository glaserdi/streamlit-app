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
    pdf.cell(0, 10, f"Dátum: {datetime.now().strftime('%Y-%m-%d')}", ln=0.5, align="C")
    pdf.cell(0, 10, f"Ajánlatot kérte: {order_data['Megrendelo_neve'].iloc[0]}", ln=0.5, align="C")
    if bevitel == "file":
        pdf.cell(0, 10,f"Sorszám: {order_data['Sorszám_Megrendelés'].iloc[0]}", ln=0.5, align="C")
    else:
        pdf.cell(0, 10, f"Sorszám: {sorszam}", ln=0.5, align="C")
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
            f"{row['Össz terület']:.2f}",
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
        total_area += row["Össz terület"]
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

    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 10, "A kis terület adalék +20%, ha a terület kisebb mint 0.3 m².", ln=1)
    pdf.cell(0, 10, "Extra méret adalék +20%, ha a terület nagyobb mint 2.5 m².", ln=1)
    pdf.cell(0, 10, "MP = Meleg peremmel", ln=1)
    pdf.cell(0, 10, "TT = Távtartóval", ln=1)
    pdf.cell(0, 10, "EF = Eltéro forma", ln=1)

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
