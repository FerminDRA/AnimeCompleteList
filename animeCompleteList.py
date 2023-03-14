import streamlit as st
import pandas as pd
import codecs
import plotly.express as px

DATA_URL = ('AnimeList.csv')

st.set_page_config(page_title="Anime Complete List",
                   page_icon="logo.jpg")
st.image("banner.jpg")

st.title("Anime Complete List")
st.header("Fermin Del Rosario Antonio")
st.header("S19004879")

st.sidebar.image("logo.jpg")
st.sidebar.markdown("##")
sidebar= st.sidebar

@st.cache
def load_data(nrows):
    f = codecs.open(DATA_URL,'r', encoding='utf-8')
    data=pd.read_csv(f,nrows=nrows)
    return data

def filtro_anime(anime):
    anime_filt = data[data['Title'].str.upper().str.contains(anime)]
    return anime_filt

def filtro_estudio(estudio):
    studio_filt = data[data['Studios'] == estudio]
    return studio_filt

data_load_state= st.text("Loading data...")
data= load_data(10000)
data_load_state.text("Done!")

titulofilme = st.sidebar.text_input('Titulo del Anime :')
botonBuscar = st.sidebar.button('Buscar Anime')

if (botonBuscar):
   peliculas = filtro_anime(titulofilme.upper())
   count_row = peliculas.shape[0]
   st.header("Animes")
   st.write(f"Total de Animes mostrados : {count_row}")
   st.write(peliculas)

selEstudio = st.sidebar.selectbox("Estudio", data['Studios'].unique())
botonFiltroEstudio = st.sidebar.button('Filtrar estudio')

if (botonFiltroEstudio):
   studio = filtro_estudio(selEstudio)
   count_row = studio.shape[0]
   st.write(f"Total de animes por estudio : {count_row}")

   st.dataframe(studio)

##Histograma
fig_episodes = px.histogram(data,
                   x="Episodes",
                   title="Numero de episodios en un Anime",
                   labels=dict(Episodes="Numero de episodios"),
                   color_discrete_sequence=["#634a71"],
                   template="plotly_white"
                   )
fig_episodes.update_layout(plot_bgcolor="rgba(0,0,0,0)")

##Grafica de barras
sourceByTitle=(
    data.groupby(by=['Source']).count()
    )
fig_source=px.bar(sourceByTitle,
                x=sourceByTitle.index,
                y="Title",
                title="Cantidad de Animes por Fuente",
                labels=dict(Title="Numero de Titulos",Source="Fuente",),
                color_discrete_sequence=["#f86749"],
                template="plotly_white")
fig_source.update_layout(plot_bgcolor="rgba(0,0,0,0)")

#Grafica Scatter
caps=data['Episodes']
scor=data['Score']
tipe=data['Type']
fig_scatter=px.scatter(data,
                         x=caps,
                         y=scor,
                         color=tipe,
                         title="Posicion por episodios",
                         labels=dict(Episodes="Episodios",Score="Calificacion", Type="Categoria"),
                         template="plotly_white")
fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)")

#Checkbox
agree=sidebar.checkbox("Mostrar graficas")
if agree:
    st.header("Histograma")
    st.plotly_chart(fig_episodes)
    st.header("Grafica de barras")
    st.plotly_chart(fig_source)
    st.header("Grafica de Scatter")
    st.plotly_chart(fig_scatter)