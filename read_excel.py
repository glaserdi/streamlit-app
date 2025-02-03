import pandas as pd
import warnings

# Figyelmeztetések elnyomása
warnings.simplefilter(action='ignore', category=UserWarning)


def extract_order_data(file_path):

    a1_value = pd.read_excel(file_path, sheet_name='Munka1', header=None, usecols="A", nrows=1).iloc[0, 0]
    g2_value = pd.read_excel(file_path, sheet_name='Munka1', header=None, usecols="G", nrows=2).iloc[1, 0]
    e5_value = pd.read_excel(file_path, sheet_name='Munka1', header=None, usecols="E", skiprows=4, nrows=1).iloc[0, 0]
    f6_value = pd.read_excel(file_path, sheet_name='Munka1', header=None, usecols="F", skiprows=5, nrows=1).iloc[0, 0]
    g6_value = pd.read_excel(file_path, sheet_name='Munka1', header=None, usecols="G", skiprows=5, nrows=1).iloc[0, 0]
    # Az adatok beolvasása a 9. sortól kezdve
    data_df = pd.read_excel(file_path, sheet_name='Munka1', header=None, skiprows=8, usecols="B,C,D,F,G,J,K")

    # Az oszlopok elnevezése
    data_df.columns = ['Szélesség', 'Magasság', 'Darabszám',
                       'Üveg típusa', 'Üveg vastagsága','Eltérő forma','Távtartó']

    # Csak a releváns sorok megtartása (ahol van üveg típusa és darabszám)
    filtered_data = data_df.dropna(subset=['Üveg típusa', 'Darabszám'], how='any').copy()

    # Új DataFrame létrehozása a plusz adatokkal
    result_data = filtered_data.assign(
        Megrendelő_neve=a1_value,
        Dátum=g2_value,
        Sorszám_Megrendelés=e5_value,
        Argon=f6_value,
        Melegperem=g6_value
    )

    return result_data
