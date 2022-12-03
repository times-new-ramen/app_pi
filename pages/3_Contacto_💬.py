import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title= "Contacto",
    page_icon= "💬",
    layout= 'centered',
)


#Fondo (Yo hice el diseño de la silueta)
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
    st.title("Aquí puedes contactar a alguno de nuestros encargados "+" "+"💬")
    st.subheader('Comunícate con nosotros')
    st.write('Pregunta a nuestros expertos sobre las vivencias internacionales')

    
    st.write('[Conoce más >](https://tec.mx/es/internacionalizacion)')



contact_form = """
<form action="https://formsubmit.co/A01337312@tec.mx" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Nombre" required>
     <input type="email" name="email" placeholder="Correo Institucional" required>
     <textarea name="message" placeholder="Escribe aquí tu mensaje"></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")
    
