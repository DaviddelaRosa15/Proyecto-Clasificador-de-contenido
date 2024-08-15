import plotly.express as px
import streamlit as st
from post import get_posts
from counter import get_country_mentions
#from model import predict_from_url, predict_from_text

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

# Streamlit app title
st.title('Visualización de Menciones de Países en Medios Latinoamericanos')

# Plot the bar chart
st.subheader('Gráfico de Barras: Presencia de los Países en los Medios')
st.plotly_chart(country_mentions_fig)

# Plot the bar chart
st.subheader('Gráfico de Barras: Fechas de las publicaciones')
st.plotly_chart(publication_dates_fig)

#input_url = input("Ingrese la URL del post: ")
#prediction = predict_from_url(input_url)
#print(f'La predicción para el post es: {prediction}')

#input_text = input("Ingrese el texto del post: ")
#prediction = predict_from_text(input_text)
#print(f'La predicción para el post es: {prediction}')