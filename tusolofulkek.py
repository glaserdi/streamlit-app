import streamlit as st
import constants as C
def show():
    st.title("🚿 Tusolófüle rendelések ")
    bevitel = st.selectbox("Hány üvegből áll a tusolófülke?", ["1", "2", "3", "Egyéb"])
    if bevitel == "1":
        osszetetel = st.selectbox("Összetétel", ["Fal", "Ajtó"])

        szelesseg = st.number_input("Szélesség (mm)", min_value=1, max_value=C.MAX_MERET,
                                    placeholder="Írj be egy számot...")
        magassag = st.number_input("Magasság (mm)", min_value=1, max_value=C.MAX_MERET,
                                    placeholder="Írj be egy számot...")
        uveg_tipus = st.selectbox("Milyen típusú üvegből szeretnéd?", ["6-os", "8-as", "Füstös", "Matt", "Fekete"])

        minta = st.selectbox("Milyen mintával szeretnéd?", ["Minta nélkül", "Telibe", "Egyszerű", "Bonyolult"])

        vasalat_szine = st.selectbox("Milyen színű vasalattal szeretnéd?", ["Inox", "Fekete", "Speciális szín"])

        szereles = st.checkbox("Szerelés a Glaserdi csapata által")

        if osszetetel == "Ajtó":
            st.balloons()
        elif osszetetel == "Fal":
            st.balloons()
    elif bevitel == "2":
        osszetetel = st.selectbox("Összetétel", ["Fal + Ajtó", "Fal + Fal", "Tolós"])

        if osszetetel == "Fal + Ajtó":
            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("A FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            magassag1 = st.number_input("A FAL magassága (mm))", min_value=1, max_value=C.MAX_MERET,
                                       placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Az AJTÓ szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Az AJTÓ magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
        elif osszetetel == "Fal + Fal":
            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("Az 1. FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Az 1. FAL magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("A 2. FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Az 1. FAL magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
        elif osszetetel == "Tolós":
            szelesseg1 = st.number_input("A FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("A FAL magassága (mm))", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Az AJTÓ szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Az AJTÓ magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")

        uveg_tipus = st.selectbox("Milyen típusú üvegekből szeretnéd?", ["6-os", "8-as", "Füstös", "Matt", "Fekete"])

        minta = st.selectbox("Milyen mintával szeretnéd?", ["Minta nélkül", "Telibe", "Egyszerű", "Bonyolult"])

        vasalat_szine = st.selectbox("Milyen színű vasalattal szeretnéd?", ["Inox", "Fekete", "Speciális szín"])

        szereles = st.checkbox("Szerelés a Glaserdi csapata által")

    elif bevitel == "3":
        osszetetel = st.selectbox("Összetétel", ["Fal + Ajtó + Fal", "Fal + Fal + Ajtó", "Fal + Ajtó + Ajtó", "Tolós"])

        if osszetetel == "Fal + Ajtó + Fal":
            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("Az 1. FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Az 1. FAL magassága (mm))", min_value=1, max_value=C.MAX_MERET,
                                       placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Az AJTÓ szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Az AJTÓ magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg3 = st.number_input("A 2. FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag3 = st.number_input("A 2. FAL magassága (mm))", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
        elif osszetetel == "Fal + Fal + Ajtó":

            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("Az 1. FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Az 1. FAL magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("A 2. FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("A 2. FAL magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg3 = st.number_input("Az AJTÓ szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag3 = st.number_input("Az AJTÓ magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")

        elif osszetetel == "Fal + Ajtó + Ajtó":

            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("Az 1. AJTÓ szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Az 1. AJTÓ magassága (mm))", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("A 2. AJTÓ szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("A 2. AJTÓ magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg3 = st.number_input("A FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag3 = st.number_input("A FAL magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")

        elif osszetetel == "Tolós":
            szelesseg1 = st.number_input("Az 1. FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Az 1. FAL magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Az AJTÓ szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Az AJTÓ magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg3 = st.number_input("A 2. FAL szélessége (mm)", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag3 = st.number_input("Az 2. FAL magassága (mm)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")

        uveg_tipus = st.selectbox("Milyen típusú üvegekből szeretnéd?", ["6-os", "8-as", "Füstös", "Matt", "Fekete"])

        minta = st.selectbox("Milyen mintával szeretnéd?", ["Minta nélkül", "Telibe", "Egyszerű", "Bonyolult"])

        vasalat_szine = st.selectbox("Milyen színű vasalattal szeretnéd?", ["Inox", "Fekete", "Speciális szín"])

        szereles = st.checkbox("Szerelés a Glaserdi csapata által")

    elif bevitel == "Egyéb":
        st.balloons()

