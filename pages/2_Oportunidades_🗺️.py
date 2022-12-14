#Importaci贸n de librer铆as

import streamlit as st
from datetime import date
import calendar
import plost
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import base64

#Configuraci贸n de P谩gina

st.set_page_config(
    page_title= "Programas Internacionales",
    page_icon= "馃憢",
    layout= 'wide',
    initial_sidebar_state='expanded'
)

st.title("Oportunidades"+" "+" 鉁堬笍")


@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

#Fondo (Yo hice el dise帽o de la silueta)
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

###Se realiza la carga de los datos a utilizar
df = pd.read_csv('tablero.csv', encoding ='latin1')
#print(df.shape)
#df.head(5)

#df['Estatus'].unique()

#Se eliminan los registros que no tengan 'Asignado' como estatus
asignados = ['Asignada','Asignada - Pendiente registrar materias','Asignada - Pendiente enviar documentos','Asignada - Materias aprobadas',
'Asignada - Materias en aprobaci贸n','Asignada - Materias enviadas a aprobaci贸n','Asignada - Materias rechazadas (2)',
'Asignada - Documentos enviados a aprobaci贸n','Asignada - Documentos aprobados','Asignada - En espera de admisi贸n',
'Asignada - Documentos a enviar', 'Asignada - Documentos en aprobaci贸n','Asignada - Materias rechazadas (1)',
'Asignada - Documentos rechazados','Asignada - Materias rechazadas (0)','Asignada - Documentos enviados','Asignada - Materias rechazadas ',
'Asignado']

df = df[df['Estatus'].isin(asignados)]
print(df.shape)
df.head(3)

#Se realiza una sustracci贸n de las primeras opciones de los diferentes estudiantes que aplicaron para la Oportunidad. 
df['1raOpcion'] = df['OportunidadesSeleccionadas'].str.split('1 - ').str[1]
df['1raOpcion'] = df['1raOpcion'].str.split(',').str[0]
print(df.shape)
df.head(3)

#Una comparaci贸n es realizada entre la columna OportunidadAsignada y 1ra Opcion para generar la columna 1raOpcionAsignada
df['1raOpcionAsignada'] = df['OportunidadAsignada'] == df['1raOpcion']
df['1raOpcionAsignada'] = df['1raOpcionAsignada'].map({True: 'Asignado', False: 'No asignado'})
print(df.shape)
df.head(3)

#Se extrae el tipo de intercambio al que pertenece la oportunidad asignada.
df['TipoInterc'] = df['OportunidadAsignada'].str.split('-').str[1]
df['TipoInterc'] = df['TipoInterc'].str.split('-').str[0]
print(df.shape)
df.head(3)


df['TipoIntercText'] = pd.np.where(df.TipoInterc.str.contains("INT"), "Intercambio Tradicional", "Study Abroad")
print(df.shape)
df.head(3)

df['PaisDestino']=df['OportunidadAsignada'].str.split('-').str[0]
print(df.shape)
df.head(3)

#df['PeriodoAcad茅mico'].unique()

#-Sesion 1, -Sesion 3, -Sesion 2, EGADE, -Sesi贸n 1, -Sesi贸n 3, Profesional, -Sesi贸n 2, de Excelencia, 

df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace(r'(\s*\(.*?\)\s*)', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('-Sesion 1', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('-Sesion 3', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico']. str.replace('-Sesion 2', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('EGADE', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('-Sesi贸n 1', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('-Sesi贸n 3', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('Profesional', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('-Sesi贸n 2', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('de Excelencia', ' ').str.strip()
df['PeriodoAcad茅mico'] = df['PeriodoAcad茅mico'].str.replace('Verano   2018', 'Verano 2018')

df['A帽oIntercambio'] = df['PeriodoAcad茅mico'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1)
print(df.shape)
df.head(3)

df['Periodo'] = df['PeriodoAcad茅mico'].str.count(' ')
print(df.shape)
df.head(3)

#df['Periodo'].unique()

#df[df['Periodo'] == 3]['PeriodoAcad茅mico'].unique()

#df[df['Periodo'] == 1]['PeriodoAcad茅mico'].unique()

#df[df['Periodo'] == 4]['PeriodoAcad茅mico'].unique()

df['PeriodoTexto'] = np.where(df['Periodo'] == 3, 'Semestre', 
                     np.where(df['Periodo'] == 1, 'Periodo Vacacional',
                     np.where(df['Periodo'] == 4, 'A帽o', 'Sin informaci贸n')))
print(df.shape)
df.head(3)

# df['PeriodoTexto'].unique()

df2 = pd.read_csv('Programas_Tec.csv')
print(df2.shape)
df2.head(3)

df = df.merge(df2, how = 'inner', left_on = 'Programa', right_on = 'Clave') 
print(df.shape)
df.head(3)

#df.columns

df = df.drop(['Nombre', 'Ap Paterno', 'Ap Materno', 'Correo Alterno', 'Celular', 'Periodo Solicitud', 'OportunidadesAprobadas', 'Estatus', 'PeriodoAcad茅mico', 
              'Actividad Actual', 'Fecha', 'TipoInterc', 'Periodo', 'Clave'], axis = 1)
print(df.shape)
df.head(3)

#df.isna().sum()

df[['Campus', 'OportunidadAsignada', 'CampusAdministrador', '1raOpcion', 'PaisDestino']] = df[['Campus', 'OportunidadAsignada', 'CampusAdministrador', '1raOpcion', 'PaisDestino']].fillna('Sin informaci贸n')
df = df.dropna()
print(df.shape)
df.head(3)

df['A帽oIntercambio'] = df['A帽oIntercambio'].astype('str').str[:4].astype('datetime64').dt.year
print(df.shape)
#df.head(3)

#Creaci贸n de columna tipos de promedio
condiciones_prom = [
    (df['Promedio'] > 90),
    (df['Promedio'] >= 80) & (df['Promedio'] <= 90),
    (df['Promedio'] < 80)
]

tipos_prom = ['Alto', 'Medio', 'Bajo']

df['PromedioTipo'] = np.select(condiciones_prom, tipos_prom)
#df.head(3)

###Gr谩ficos
df['PaisDestino'].unique()
paises_coords= pd.read_csv('paises_coords.csv')

#Sankey Graph
#df['Nivel'].unique()

df_sankey= df.groupby(["Nivel","PromedioTipo"])["Matr铆cula"].count().reset_index()
df_sankey.columns= ['source','target','value']
#df_sankey.head(3)

df_sankey2= df.groupby(["PromedioTipo","1raOpcionAsignada"])["Matr铆cula"].count().reset_index()
df_sankey2.columns= ['source','target','value']
#df_sankey2.head(3)

links= pd.concat([df_sankey,df_sankey2], axis=0)
#links

unique_source_target= list (pd.unique(links[['source', 'target']].values.ravel('K')))
#unique_source_target

mapping_dict= {k: v for v, k in enumerate(unique_source_target)}
#mapping_dict

links['source']=  links['source'].map(mapping_dict)
links['target']=  links['target'].map(mapping_dict)

links_dict= links.to_dict(orient='list')
links_dfs1= links.to_dict(orient='list')
links_dfs2= links.to_dict(orient='list')
#links_dict

st.header("驴Cu谩ntas personas van a Programas Internacionales?")
#Figura Sankey
fig_sankey = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "purple", width = 0.5),
      label = unique_source_target,
      color = "darkblue"
    ),
    link = dict(
      source = links_dict["source"],
      target = links_dict["target"],
      value = links_dict["value"]
  ))])

label_int_snk= links.keys()
#label_int_snk

label_int_snk= list(links_dfs1.keys()) + list(links_dfs2.keys())
#links_dict

value= list(links_dfs1.values()) + list(links_dfs2.values()) 
#value

source= list (range(len(links_dfs1))) + [len(links_dfs1)] * len(links_dfs2)
#source

target= [len(links_dfs1)] * len(links_dfs1) + [label_int_snk.index(links_dfs2) for links_dfs2 in links_dfs2.keys()]
#target


fig_sankey.update_layout(title_text="Asignaci贸n por Promedio y Nivel Educativo", font_size=10)
st.plotly_chart(fig_sankey)

### PIE CHART
nombres_pie= list(df['1raOpcionAsignada'].unique())
valores_pie= list(df['1raOpcionAsignada'].value_counts())
fig_pie = go.Figure(data = [go.Pie(labels = nombres_pie, values = valores_pie, hole = 0.5)])

st.header("Alumnos en su Primera Opci贸n")
fig_pie.update_layout(title_text="Alumnos en Primera Opci贸n", font_size=8)
st.plotly_chart(fig_pie)

###BARRAS CHART
x_bar= list(df['Campus'].unique())
y_bar= list(df['PromedioTipo'].value_counts())
fig_barras = go.Figure(data = [go.Bar(x=x_bar, y = y_bar)])

st.header("Nivel de Promedio por Campus")
fig_barras.update_layout(title_text="Promedio por Campus", font_size=8)
st.plotly_chart(fig_barras)

st.header("驴Qu茅 me muestran estos datos?")
st.write("Los datos mostrados arriba pertenecen a todos los alumnos que han aplicado para Programas Internacionales satisfactoriamente.")
st.header("驴C贸mo puedo usar esta informaci贸n? ")
st.write("Inf贸rmate sobre las tendencias en promedio ,nivel acad茅mico ,campus, carrera, entre otros; esto te ayudar谩 a tomar decisiones que se ajusten a tu criterio y necesidades.")

#Sidebar
sidebar = st.sidebar
sidebar.title("Datos din谩micos")
sidebar.write("Selecciona los ajustes de tu preferencia")

# Display the content of the dataset if checkbox is true
st.header("Dataset")
agree = sidebar.checkbox("Ense帽ar muestra de dataset ")
if agree:

    #Barra pa铆s
    selected_country = sidebar.selectbox("Selecciona un pa铆s:",
    df['PaisDestino'].unique())
    st.success(f'Seleccionaste {selected_country}')
    st.markdown("___")

    selected_campus = sidebar.selectbox("Selecciona un Campus:",
    df['Campus'].unique())
    st.success(f'Seleccionaste {selected_campus}')
    st.markdown("___")

    optionals = sidebar.expander("Configuraciones Opcionales", True)
    fecha_select = optionals.slider(
    "Selecciona la fecha",
    min_value=int(df['A帽oIntercambio'].min()),
    max_value=int(df['A帽oIntercambio'].max())
    )

    subset_fecha =df[df['A帽oIntercambio'] == (fecha_select)]
    st.write(f"Registros {fecha_select}: {subset_fecha.shape[0]}")
    st.dataframe(subset_fecha)
    st.markdown("___")

