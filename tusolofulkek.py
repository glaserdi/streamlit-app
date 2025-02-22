import streamlit as st
import constants as C
def show():

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

            szelesseg1 = st.number_input("Szélessége (mm) a falnak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Magassága (mm) a falnak)", min_value=1, max_value=C.MAX_MERET,
                                       placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Szélessége (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Magassága (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
        elif osszetetel == "Fal + Fal":
            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("Szélessége (mm) az első falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Magassága (mm) az első falnak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Szélessége (mm) a második falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Magassága (mm) a második falnak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
        elif osszetetel == "Tolós":
            szelesseg1 = st.number_input("Szélessége (mm) a falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Magassága (mm) a falnak)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Szélessége (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Magassága (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")

        uveg_tipus = st.selectbox("Milyen típusú üvegekből szeretnéd?", ["6-os", "8-as", "Füstös", "Matt", "Fekete"])

        minta = st.selectbox("Milyen mintával szeretnéd?", ["Minta nélkül", "Telibe", "Egyszerű", "Bonyolult"])

        vasalat_szine = st.selectbox("Milyen színű vasalattal szeretnéd?", ["Inox", "Fekete", "Speciális szín"])

        szereles = st.checkbox("Szerelés a Glaserdi csapata által")

    elif bevitel == "3":
        osszetetel = st.selectbox("Összetétel", ["Fal + Ajtó + Fal", "Fal + Fal + Ajtó", "Fal + Ajtó + Ajtó", "Tolós"])

        if osszetetel == "Fal + Ajtó + Fal":
            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("Szélessége (mm) az első falnak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Magassága (mm) az első falnak)", min_value=1, max_value=C.MAX_MERET,
                                       placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Szélessége (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Magassága (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg3 = st.number_input("Szélessége (mm) a második falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag3 = st.number_input("Magassága (mm) a második falnak)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
        elif osszetetel == "Fal + Fal + Ajtó":

            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("Szélessége (mm) az első falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Magassága (mm) az első falnak)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Szélessége (mm) a második falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Magassága (mm) a második falnak)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg3 = st.number_input("Szélessége (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag3 = st.number_input("Magassága (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")

        elif osszetetel == "Fal + Ajtó + Ajtó":

            tipus = st.radio("Típus?", ["L alakú", "Egymás melletti"])

            szelesseg1 = st.number_input("Szélessége (mm) az első ajtónak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Magassága (mm) az első ajtónak)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Szélessége (mm) a második ajtónak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Magassága (mm) a második ajtónak)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg3 = st.number_input("Szélessége (mm) a falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag3 = st.number_input("Magassága (mm) a falnak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")

        elif osszetetel == "Tolós":
            szelesseg1 = st.number_input("Szélessége (mm) az első falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag1 = st.number_input("Magassága (mm) az első falnak)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg2 = st.number_input("Szélessége (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag2 = st.number_input("Magassága (mm) az ajtónak", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")
            szelesseg3 = st.number_input("Szélessége (mm) a második falnak", min_value=1, max_value=C.MAX_MERET,
                                         placeholder="Írj be egy számot...")
            magassag3 = st.number_input("Magassága (mm) a második falnak)", min_value=1, max_value=C.MAX_MERET,
                                        placeholder="Írj be egy számot...")

        uveg_tipus = st.selectbox("Milyen típusú üvegekből szeretnéd?", ["6-os", "8-as", "Füstös", "Matt", "Fekete"])

        minta = st.selectbox("Milyen mintával szeretnéd?", ["Minta nélkül", "Telibe", "Egyszerű", "Bonyolult"])

        vasalat_szine = st.selectbox("Milyen színű vasalattal szeretnéd?", ["Inox", "Fekete", "Speciális szín"])

        szereles = st.checkbox("Szerelés a Glaserdi csapata által")

    elif bevitel == "Egyéb":
        st.balloons()

