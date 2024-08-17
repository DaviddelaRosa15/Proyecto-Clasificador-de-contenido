# Clasificación de Noticias Latinoamericanas

Este proyecto tiene como objetivo clasificar contenido de noticias en diferentes categorías utilizando un modelo de aprendizaje automático. A continuación, se detallan los pasos para instalar y ejecutar la aplicación.

## Requisitos

- Python 3.7 o superior
- Los paquetes listados en `requirements.txt`
- Conexión a internet para descargar el módulo de lenguaje de Spacy

## Instalación

Sigue estos pasos para configurar el entorno y ejecutar la aplicación:

### 1. Clonar el Repositorio

Primero, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

### 2. Instalar Dependencias

Instala los paquetes requeridos utilizando el archivo requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Descargar el Módulo de Lenguaje Inglés de Spacy
El proyecto utiliza Spacy para procesamiento de lenguaje natural. Necesitas descargar el módulo de lenguaje inglés:

```bash
python -m spacy download en_core_web_sm
```

### 4. Colocar el Archivo data_train.csv
Asegúrate de que el archivo data_train.csv esté en la ruta especificada en el repositorio. Si deseas agregar más datos para el entrenamiento, coloca el archivo en la misma ubicación:

ruta/a/tu/proyecto/data_train.csv

### 5. Ejecutar la Aplicación
Por último, ejecuta el siguiente comando para iniciar la aplicación en Streamlit:

```bash
streamlit run app.py
```

## Uso de la Aplicación
La aplicación Streamlit permitirá:

Visualizar el análisis exploratorio de datos (EDA): Sección donde se muestran gráficos de la distribución de menciones por país y fechas de publicación.
Interacción con el modelo: Los usuarios pueden clasificar nuevas noticias ingresando la URL de Reddit o el texto de la noticia.
Revisión de la precisión del modelo: Sección que muestra la precisión del modelo en los datos de entrenamiento y prueba.
