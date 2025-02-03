from fpdf import FPDF
from datetime import datetime
import pandas as pd
import io

# PDF generáló osztály
def generate_pdf(order_data, company_name, company_logo_path, output_path="arajanlat.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Cég logó és név
    pdf.image(company_logo_path, x=10, y=8, w=30)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, company_name, ln=1, align="C")

    # Árajánlat cím és dátum
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ÁRAJÁNLAT", ln=1, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Dátum: {datetime.now().strftime('%Y-%m-%d')}", ln=1, align="C")
    pdf.cell(0, 10, f"Megrendelo neve: {order_data['Megrendelo_neve'].iloc[0]}", ln=1, align="C")
    # Táblázat fejléc
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "Üveg típusa", 1)
    pdf.cell(30, 10, "Terület (m²)", 1)
    pdf.cell(30, 10, "Adalék", 1)
    pdf.cell(30, 10, "Összterület", 1)
    pdf.cell(30, 10, "Egységár", 1)
    pdf.cell(40, 10, "Ár (lei)", 1)
    pdf.ln()

    # Táblázat adatok
    pdf.set_font("Arial", "", 12)
    total_price = 0
    total_area = 0

    for index, row in order_data.iterrows():
        pdf.cell(40, 10, str(row["Üveg típusa"]), 1)
        pdf.cell(30, 10, f"{row['Terület']:.2f}", 1)
        pdf.cell(30, 10, f"{row['Adalék']:.2f}", 1)
        pdf.cell(30, 10, f"{row['Össz terület']:.2f}", 1)
        pdf.cell(30, 10, f"{row['Egységár']:.2f}", 1)
        pdf.cell(40, 10, f"{row['Ár']:.0f} lei", 1)
        pdf.ln()

        total_area += row["Össz terület"]
        total_price += row["Ár"]

    # Összesített ár
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Összesen:", 1)
    pdf.cell(40, 10, f"{total_area:.0f} m²", 1)
    pdf.cell(40, 10, f"{total_price:.0f} lei", 1)

    # Mentés
    buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer = io.BytesIO(pdf_output)
    buffer.seek(0)
    return buffer

# Példa DataFrame
order_data = pd.DataFrame({
    "Üveg típusa": ["F4-Low-e4", "Float 6 mm"],
    "Terület": [2.5, 3.0],
    "Adalék": [0.2, 0.3],
    "Ár": [25000, 30000]
})


