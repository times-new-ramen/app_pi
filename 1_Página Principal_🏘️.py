import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title= "Programas Internacionales",
    page_icon= "👋",
    layout= 'wide',
    initial_sidebar_state='expanded'
)

#Fondo(Yo hice el diseño de la silueta)

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("pi.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: 100%;
background-position: bottom;
background-repeat: no-repeat;
background-attachment: local;
}}
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


#Encabezado
with st.container():
    st.title("Bienvenido a PI "+" "+"👋")
    st.subheader('¡Vive una experiencia sin igual!')
    st.write('Encuentra toda la información que necesites sobre las vivencias internacionales')
    st.write('[Conoce más >](https://tec.mx/es/internacionalizacion)')

###Mapa
df = pd.read_csv('tablero.csv', encoding ='latin1')
paises_coords= pd.read_csv('paises_coords.csv')
st.map(data=paises_coords,zoom=0)

st.header("¡Conoce tus opciones!")
st.write("El mapa desplegado muestra todos los países a los que ha llegado Programas Internacionales. ¡Únete a esta única experiencia!")


