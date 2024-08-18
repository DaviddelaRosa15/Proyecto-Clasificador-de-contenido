import plotly.express as px
import streamlit as st
import pandas as pd
from post import get_posts
from counter import get_country_mentions
from model import train_df, accuracy_train, accuracy_test, unique_targets, cm_train_df, cm_test_df, predict_from_url, predict_from_text
from confusion_matrix import plot_confusion_matrix

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

# Sección 3: Datos de Entrenamiento y Precisión del Modelo
st.header('Datos de Entrenamiento y Precisión del Modelo')

# Ejemplo de datos de entrenamiento
st.subheader('Resumen de los Datos de Entrenamiento')
st.write("Aquí se presentan algunos datos usados para entrenar el modelo:")
st.write(train_df.head(10))

st.subheader("Categorías Utilizadas para el Modelo")

# Obtener y mostrar las categorías distintas
if 'target' in train_df.columns:
    # Crear una lista con las categorías para mostrar
    categories_list = "<ul>" + "".join([f"<li>{category}</li>" for category in unique_targets]) + "</ul>"
    
    # Mostrar las categorías
    st.write("Las categorías en las que se trabajará son las siguientes:")
    st.markdown(categories_list, unsafe_allow_html=True)

    # Contar el número de categorías distintas
    num_categories = len(unique_targets)
    st.write(f"Número de categorías distintas: {num_categories}")

      # Contar la cantidad de noticias por cada categoría
    category_counts = train_df['target'].value_counts()
    
    # Crear un gráfico de barras horizontales con Plotly
    fig = px.bar(category_counts, 
                 x=category_counts.values, 
                 y=category_counts.index,
                 orientation='h',
                 color=category_counts.values,
                 color_continuous_scale='Viridis',
                 labels={'x': 'Cantidad de Noticias', 'y': 'Categoría'},
                 title='Cantidad de Noticias por Categoría',
                 text=category_counts.values,
                 text_auto=True)
    
    # Personalizar el diseño del gráfico
    fig.update_layout(
        title_font_size=24,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_title_font_size=16,
        font_size=14,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    
    st.plotly_chart(fig)
else:
    st.write("La columna 'target' no se encuentra en el archivo CSV. Por favor, revisa el archivo.")

# Precisión del modelo
st.subheader('Precisión del Modelo')

accuracy_data = pd.DataFrame({
    'Conjunto de Datos': ['Entrenamiento', 'Prueba'],
    'Precisión': [accuracy_train, accuracy_test]
})

st.write("Precisión del modelo en diferentes conjuntos de datos:")
fig = px.bar(accuracy_data, x='Conjunto de Datos', y='Precisión', color='Conjunto de Datos', 
             text='Precisión', height=400)
fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')
fig.update_yaxes(range=[0, 1])
st.plotly_chart(fig)

# Mostrar la matriz de confusión para los datos de entrenamiento
cm_train_fig = plot_confusion_matrix(cm_train_df, 'Matriz de Confusión - Datos de Entrenamiento')
st.plotly_chart(cm_train_fig)

# Mostrar la matriz de confusión para los datos de prueba
cm_test_fig = plot_confusion_matrix(cm_test_df, 'Matriz de Confusión - Datos de Prueba')
st.plotly_chart(cm_test_fig)

# Sección 4: Interacción con el Modelo
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

# Nueva sección de Resultados
st.subheader('Resultados')

# Obtener la categoría más frecuente
most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

st.write("En base a los datos de entrenamiento que obtuvimos de **Reddit**, la categoría de noticias sobre la cual más se habla es la siguiente:")
st.write(f"**Categoría predominante:** {most_common_category}")
st.write(f"**Número de noticias clasificadas:** {most_common_count}")

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