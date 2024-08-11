import pandas as pd
from collections import Counter

# Definir la lista de países latinoamericanos
latin_american_countries = [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica",
    "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala",
    "Honduras", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru",
    "Puerto Rico", "Uruguay", "Venezuela"
]

def count_country_mentions(text, countries):
    mentions = Counter()
    for country in countries:
        if country.lower() in text.lower():
            mentions[country] += 1
    return mentions

def get_country_mentions(df):
    # Contar menciones en títulos y textos
    country_mentions = Counter()
    for index, row in df.iterrows():
        title_mentions = count_country_mentions(row['title'], latin_american_countries)
        text_mentions = count_country_mentions(row['selftext'], latin_american_countries)
        country_mentions.update(title_mentions)
        country_mentions.update(text_mentions)

    # Convertir el resultado a un DataFrame para su visualización
    country_mentions_df = pd.DataFrame.from_dict(country_mentions, orient='index', columns=['mentions']).reset_index()
    country_mentions_df.columns = ['country', 'mentions']
    country_mentions_df = country_mentions_df.sort_values(by='mentions', ascending=False)

    return country_mentions_df