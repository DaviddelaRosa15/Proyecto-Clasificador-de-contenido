import praw
import pandas as pd
import streamlit as st

# Configura tus credenciales de Reddit
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
user_agent = st.secrets["user_agent"]

# Autenticación con Reddit
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

def get_posts(query, subreddit, limit=100):
  # Buscar posts en Reddit
  posts = []
  for submission in reddit.subreddit(subreddit).search(query, limit=100):
      posts.append({
          'title': submission.title,
          'selftext': submission.selftext,
          'author': str(submission.author),
          'score': submission.score,
          'created_utc': submission.created_utc,
          'num_comments': submission.num_comments,
          'url': submission.url
      })

  # Convertir los posts en un DataFrame de Pandas
  df = pd.DataFrame(posts)

  # Convertir timestamps a fechas legibles
  df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')

  # Eliminar filas con valores nulos en las columnas 'title' y 'selftext'
  df.dropna(subset=['title', 'selftext'], inplace=True)

  # Eliminar duplicados basados en los títulos de los posts
  df.drop_duplicates(subset=['title'], inplace=True)

  return df

def get_post_url(url):
  # Obtener información del post a partir de su URL
  submission = reddit.submission(url=url)

  post = {
      'title': submission.title,
      'selftext': submission.selftext
  }
  return post