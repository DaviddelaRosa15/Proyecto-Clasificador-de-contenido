import matplotlib.pyplot as plt
import seaborn as sns
from post import get_posts
from counter import get_country_mentions
from model import predict_from_url, predict_from_text

# Definir la búsqueda
query = 'latinoamericans countries'
subreddit = 'all'

df = get_posts(query, subreddit)

country_mentions_df = get_country_mentions(df)

print(country_mentions_df)

# Gráfico de la distribución de fechas de publicación
plt.figure(figsize=(10, 6))
df['created_utc'].hist(bins=30)
plt.title('Distribución de Fechas de Publicación')
plt.xlabel('Fecha')
plt.ylabel('Número de Posts')
plt.show()

# Visualización de menciones de países
plt.figure(figsize=(11, 8))
sns.barplot(x='mentions', y='country', data=country_mentions_df, palette='viridis')
plt.title('Presencia de los países latinoamericanos en los medios')
plt.xlabel('Número de Menciones')
plt.ylabel('País')
plt.show()

input_url = input("Ingrese la URL del post: ")
prediction = predict_from_url(input_url)
print(f'La predicción para el post es: {prediction}')

input_text = input("Ingrese el texto del post: ")
prediction = predict_from_text(input_text)
print(f'La predicción para el post es: {prediction}')