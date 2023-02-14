## Web Scraping en el Journal of Macroeconomics
## Limpieza de los datos

# !pip install wordcloud
# import nltk
# nltk.download('stopwords')

import pandas as pd
import re
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

import warnings
warnings.simplefilter("ignore")


dta = pd.read_pickle("./data/dta.pkl")
dta.head()


## Correcciones ===============================================================
dta = dta[dta["authors"].map(lambda d: len(d)) > 0]
dta["volume_date"] = dta["volume_date"].str.replace(r'[^(]*\(|\)[^)]*', '')
dta["volume_name"] = dta["volume_name"].str.split(',').str[0]
dta["year"] = dta["volume_date"].str.split().str[-1]
dta.reset_index(inplace=True)
dta.drop("index", axis=1, inplace=True)


## Creación de Keywords =======================================================
dta["keywords"] = dta["article_name"].str.lower()

# Eliminar palabras -> stopwords
dta["keywords"] = dta["keywords"] \
    .str.replace(r"\s*(?<!\w)(?:{})(?!\w)"
                 .format("|".join([re.escape(x) for x in stops])), " ")

# Eliminar caracteres
characters = [":", ",", ".", ";", '“','”',"'"]
for c in characters:
    dta["keywords"] = dta["keywords"].str.replace(c, '')

# Palabras a lista
dta["keywords"] = dta["keywords"].str.replace(r'\s+', ' ', regex=True)
dta["keywords"] = dta["keywords"].str.strip()
dta["keywords"] = [x.split(" ") for x in dta["keywords"]]

# Eliminando el titulo
dta.drop(["article_name"], axis=1, inplace=True)


## Guardado
dta.to_pickle("./data/dta_f.pkl")
dta.to_csv("./data/dta_f.csv", sep=';')
