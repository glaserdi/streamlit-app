import streamlit as st
import page1
import page3
# Sidebar navigáció
st.set_page_config(layout="wide")
st.sidebar.title("Navigáció")
page = st.sidebar.radio("Válassz egy oldalt:", ["Főoldal", "Termó számítások", "Vágott üveg számítások"])

# Oldalak betöltése
if page == "Főoldal":
    st.title("Üdvözöllek a Streamlit alkalmazásban!")
    st.write("Ez egy többoldalas alkalmazás példája.")

elif page == "Termó számítások":
    page1.show()

elif page == "Vágott üvegek":
    page3.show()

