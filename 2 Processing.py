## Web Scraping en el Journal of Macroeconomics
## Limpieza de los datos

# import nltk
# nltk.download('stopwords')

import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

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

# Eliminar palabras -> stopwords y caracteres
stops = set(stopwords.words('english'))

dta["keywords"] = dta["keywords"].apply(word_tokenize)
dta["keywords"] = dta["keywords"].apply( lambda x: [w for w in x if w not in stops] )
dta["keywords"] = dta["keywords"].apply( lambda x: [w for w in x if w not in string.punctuation] )
dta["keywords"] = dta["keywords"].apply( lambda x: [w for w in x if w not in ['“', '”']] )

# Eliminando el titulo
dta.drop(["article_name"], axis=1, inplace=True)

# Quitando observaciones que no son articulos =================================
dta = dta[  dta["keywords"].apply(lambda x: x.count("editorial") == 0)  ]
dta = dta[  dta["keywords"].apply(lambda x: x.count("isbn") == 0)       ]
dta = dta[  dta["keywords"].apply(lambda x: x.count("foreword") == 0)   ]
dta = dta[  dta["keywords"].apply(lambda x: x != ['editor'])            ]


## Guardado
dta.to_pickle("./data/dta_f.pkl")
dta.to_csv("./data/dta_f.csv", sep=';')
