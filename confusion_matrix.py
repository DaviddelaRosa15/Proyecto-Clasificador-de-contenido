import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Función para crear y mostrar matrices de confusión
def plot_confusion_matrix(cm_df, title):
    fig = ff.create_annotated_heatmap(
        z=cm_df.values,
        x=cm_df.columns.tolist(),
        y=cm_df.index.tolist(),
        colorscale='Viridis',
        showscale=True
    )
    fig.update_layout(title=title, xaxis_title='Predicción', yaxis_title='Verdadera Etiqueta')

    fig.update_layout(
        title=title,
        xaxis_title='Predicción',
        yaxis_title='Verdadera Etiqueta',
        xaxis=dict(tickangle=-25),  # Ajustar el ángulo de las etiquetas del eje x
        yaxis=dict(tickangle=0),    # Ajustar el ángulo de las etiquetas del eje y
        margin=dict(l=100, r=50, t=250, b=100),  # Ajustar los márgenes del gráfico
        height=600,  # Ajustar la altura del gráfico
        width=800     # Ajustar el ancho del gráfico
    )
    return fig