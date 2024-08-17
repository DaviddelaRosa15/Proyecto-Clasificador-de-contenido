from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
import spacy
import pandas as pd
from post import get_post_url

#Colocando el idioma de inglés
nlp = spacy.load("en_core_web_sm")

#Funcion para preprocesar el texto
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return ' '.join(tokens)

#Creando el dataframe para entrenar el modelo
train_df = pd.read_csv('data_train.csv')

#Separando los datos de entrenamiento y evaluación para el modelo
X_train, X_test, y_train, y_test = train_test_split(
    train_df['processed_text'], train_df['target'],
    test_size=0.2,
    random_state=42
)

#Haciendo el pipeline para el modelo
model = make_pipeline(CountVectorizer(), MultinomialNB())

#Entrenando el modelo
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy_test = accuracy_score(y_test, y_pred)
print(f'Precisión del modelo con los datos de prueba: {int(round(accuracy_test, 2)*100)}%')

y_pred_train = model.predict(X_train)
accuracy_train = accuracy_score(y_train, y_pred_train)
print(f'Precisión del modelo con los datos de entrenamiento: {int(round(accuracy_train, 2)*100)}%')

def predict_from_url(url):
    post = get_post_url(url)
    processed_text = preprocess_text(post['title'] + ': ' + post['selftext'])
    prediction = model.predict([processed_text])[0]
    return prediction

def predict_from_text(text):
    processed_text = preprocess_text(text)
    prediction = model.predict([processed_text])[0]
    return prediction