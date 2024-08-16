import plotly.express as px
import streamlit as st
from post import get_posts
from counter import get_country_mentions
from model import predict_from_url, predict_from_text

# Definir la búsqueda
query = 'latinoamericans countries'
subreddit = 'all'

df = get_posts(query, subreddit)

country_mentions_df = get_country_mentions(df)

print(country_mentions_df)

# Creando el gráfico de barras para la presencia de los países latinos encontrados en los posts
country_mentions_fig = px.bar(
    country_mentions_df,
    x='mentions',
    y='country',
    orientation='h',
    color='country',
    color_continuous_scale='Viridis',
    labels={'mentions': 'Número de Menciones', 'country': 'País'},
    title='Presencia de los Países Latinoamericanos en los Medios'
)

country_mentions_fig.update_layout(
    xaxis_title='Número de Menciones',
    yaxis_title='País',
    showlegend=False,
    height=600,
    width=800
)

# Creando el gráfico de distribución de fechas de publicación de los posts
publication_dates_fig = px.histogram(
    df, 
    x='created_utc', 
    nbins=30, 
    title='Distribución de Fechas de Publicación', 
    labels={'created_utc': 'Fecha'},
    color_discrete_sequence=['#636EFA'] 
)

publication_dates_fig.update_layout(
    xaxis_title='Fecha',
    yaxis_title='Número de Posts',
    bargap=0.2,  # Gap between bars
    height=600,
    width=800
)

# Título del sitio
st.title('Clasificación de Noticias Latinoamericanas')

# Sección 1: Explicación del Proyecto
st.header('Sobre el Proyecto')
st.write("""
Este proyecto tiene como objetivo clasificar contenido de noticias en diferentes categorías utilizando un modelo de aprendizaje automático.
A lo largo de este sitio, exploraremos los datos, visualizaremos el análisis exploratorio de datos (EDA) y proporcionaremos una interfaz
para que los usuarios interactúen con el modelo y clasifiquen nuevas noticias.
""")

# Sección 2: Visualizaciones del EDA
st.header('Análisis Exploratorio de Datos (EDA)')
st.write("En esta sección, presentamos algunos gráficos que nos ayudan a entender mejor la distribución y las características de las noticias recopiladas.")

# Primer gráfico
st.subheader('Gráfico de Barras: Presencia de los Países en los Medios')
st.write("El primer gráfico muestra la presencia de los países latinoamericanos en los medios de comunicación. Este análisis nos permite visualizar qué países tienen más menciones en las noticias, lo cual puede reflejar la relevancia mediática de estos países en un período específico.")
st.plotly_chart(country_mentions_fig)

# Segundo gráfico   
st.subheader('Gráfico de Barras: Fechas de las publicaciones')
st.write("El segundo gráfico analiza la distribución temporal de las noticias recopiladas. Al observar las fechas de publicación, podemos identificar patrones temporales, como picos de actividad mediática, que pueden estar relacionados con eventos importantes o tendencias en la región.")
st.plotly_chart(publication_dates_fig)

# Sección 3: Interacción con el Modelo
st.header('Modelo Clasificador de Noticias')
st.write("""
Para clasificar nuevas noticias, utilice la interfaz que se proporciona a continuación. Ingrese la URL o el texto de la noticia, y el modelo automático clasificará la noticia según las características de su contenido.
""")

# Acordeón para el método de URL de Reddit
with st.expander("Clasificar por URL de Reddit"):
    reddit_url = st.text_input("Ingresa la URL de Reddit:")
    if st.button('Clasificar URL'):
        if reddit_url:
            st.write(f"Clasificando la URL: *{reddit_url}*")

            #Llamando al modelo para clasificar la URL del post
            prediction = predict_from_url(reddit_url)

            st.subheader('Categoría Predicha')
            st.write(f'La noticia pertenece a la categoría: **{prediction}**')
        else:
            st.write("Por favor, ingresa una URL válida.")

# Acordeón para el método de texto
with st.expander("Clasificar por Texto"):
    user_input = st.text_area("Ingresa el texto de la noticia que deseas clasificar:")
    if st.button('Clasificar Texto'):
        if user_input:
            #Llamando al modelo para clasificar el texto
            prediction = predict_from_text(user_input)

            # Mostrar la predicción
            st.subheader('Categoría Predicha')
            st.write(f'La noticia pertenece a la categoría: **{prediction}**')
        else:
            st.write("Por favor, ingresa el texto de la noticia.")

st.header('Acerca de')
st.write("""
Este proyecto fue desarrollado por:

- **David de la Rosa**
- **Juan Guzman**
- **Gabriela Cabrera**
- **Dalvin Molina**

Somos un equipo comprometido con el análisis y la clasificación de contenidos mediáticos en el contexto latinoamericano, utilizando las últimas técnicas en aprendizaje automático.

Gracias por compartirnos sus conocimientos en este viaje por el mundo de los datos y la tecnología.
""")