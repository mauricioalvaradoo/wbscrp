## Web Scraping en el Journal of Macroeconomics
## Limpieza de los datos

# !pip install wordcloud
# import nltk
# nltk.download('stopwords')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wordcloud import WordCloud

import re
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

import warnings
warnings.simplefilter("ignore")


dta = pd.read_pickle("./data/dta.pkl")
dta.head()


## Correcciones ===============================================================
dta.dropna(axis=0, inplace=True)
dta["volume_date"] = dta["volume_date"].str.replace(r'[^(]*\(|\)[^)]*', '')
dta["volume_name"] = dta["volume_name"].str.split(',').str[0]
dta["year"] = dta["volume_date"].str.split().str[-1]
# dta["authors"] = dta["authors"].str[1:]
# dta["authors"] = dta["authors"].str[:-1]
# dta["authors"] = dta["authors"].str.replace("'", "")


## Creación de Keywords =======================================================
dta["keywords"] = dta["article_name"].str.lower()

# Eliminar palabras
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



## Estadísticas ===============================================================
print(f"Filas: {dta.shape[0]}\nColumnas:{dta.shape[1]}")


print("El TOP 10 de mayor cantidad de publicaciones por fecha es:")
print("")
print(dta["volume_date"].value_counts()[0:10])


print("El TOP 10 de mayor cantidad de publicaciones por volumen es:")
print("")
print(dta[["volume_name"]].value_counts()[0:10])


print("El TOP 10 de mayor cantidad de publicaciones por año es:")
print("")
print(dta[["year"]].value_counts()[0:10])



## Visualización ==============================================================
### Cantidad de publicaciones por año
publication_per_year = dta[["year", "volume_date"]].groupby("year").count()
colors = ["red" if index == "2008" else "gray" for index in publication_per_year.index]

fig, ax = plt.subplots(figsize=(10,5))
fig = plt.bar(
    x=publication_per_year.index, height=publication_per_year.volume_date,
    color=colors, alpha=0.5
)

plt.title("Cantidad de publicaciones por año", fontsize=15)
plt.xlabel("")
plt.grid(linestyle='--')
plt.tick_params(direction='in', which='both', length=9, width=1, labelsize=12)
ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
plt.tight_layout()

plt.savefig("./figures/bar-publicaciones-year.pdf")
plt.savefig("./figures/bar-publicaciones-year.png")
plt.show()


### Wordcloud: Palabras más usadas
words_per_year = dta.explode("keywords")[["year", "keywords"]]
text = words_per_year["keywords"].value_counts().to_dict()
wordcloud = WordCloud(
    width=1600, height=800, max_font_size=150, max_words=200,
    background_color="white"
).generate_from_frequencies(text)

plt.figure(figsize=(10,5), facecolor='k')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)

plt.savefig("./figures/wordcloud-keywords.pdf")
plt.savefig("./figures/wordcloud-keywords.png")
plt.show()


{k: text[k] for k in list(text)[:10]} ### Top 10


### Cantidad de apariciones de la palabra "policy"
policy_per_year = words_per_year[words_per_year["keywords"] == "policy"]
policy_per_year = policy_per_year.groupby("year").count()

colors = ["red" if index == "2004" else "gray" for index in policy_per_year.index]

fig, ax = plt.subplots(figsize=(10,5))
fig = plt.bar(
    x=policy_per_year.index, height=policy_per_year.keywords,
    color=colors, alpha=0.5
)

plt.title("Cantidad de apariciones de la palabra 'policy'", fontsize=15)
plt.xlabel("")
plt.grid(linestyle='--')
plt.tick_params(direction='in', which='both', length=9, width=1, labelsize=12)
ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
plt.tight_layout()

plt.savefig("./figures/bar-policy-year.pdf")
plt.savefig("./figures/bar-policy-year.png")
plt.show()


### Cantidad de apariciones de la palabra "growth"
growth_per_year = words_per_year[words_per_year["keywords"] == "growth"]
growth_per_year = growth_per_year.groupby("year").count()
colors = ["red" if index == "2008" else "gray" for index in growth_per_year.index]

fig, ax = plt.subplots(figsize=(10,5))
fig = plt.bar(
    x=growth_per_year.index, height=growth_per_year.keywords,
    color=colors, alpha=0.5
)

plt.title("Cantidad de apariciones de la palabra 'growth'", fontsize=15)
plt.xlabel("")
plt.grid(linestyle='--')
plt.tick_params(direction='in', which='both', length=9, width=1, labelsize=12)
ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
plt.tight_layout()

plt.savefig("./figures/bar-growth-year.pdf")
plt.savefig("./figures/bar-growth-year.png")
plt.show()


### Cantidad de apariciones de la palabra "monetary"
monetary_per_year = words_per_year[words_per_year["keywords"] == "monetary"]
monetary_per_year = monetary_per_year.groupby("year").count()
colors = ["red" if index == "2004" else "gray" for index in monetary_per_year.index]

fig, ax = plt.subplots(figsize=(10,5))
fig = plt.bar(
    x=monetary_per_year.index, height=monetary_per_year.keywords,
    color=colors, alpha=0.5
)

plt.title("Cantidad de apariciones de la palabra 'monetary'", fontsize=15)
plt.xlabel("")
plt.grid(linestyle='--')
plt.tick_params(direction='in', which='both', length=9, width=1, labelsize=12)
ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
plt.tight_layout()

plt.savefig("./figures/bar-monetary-year.pdf")
plt.savefig("./figures/bar-monetary-year.png")
plt.show()


### TOP 15 de autores con más publicaciones
# Separando autores
authors = dta["authors"].values.tolist()
authors = [x.split("], ") for x in authors]
authors = sum(authors, [])
# Limpiando elementos
authors = [s.replace("[", "") for s in authors]
authors = [s.replace("]", "") for s in authors]
# Agrupando
publication_per_author = {x:authors.count(x) for x in authors}
publication_per_author = dict(sorted(publication_per_author.items(), key=lambda item: item[1], reverse=True))
# TOP 20
publication_per_author = {k: publication_per_author[k] for k in list(publication_per_author)[:15]}
y = publication_per_author.keys()
x = publication_per_author.values()

pos = np.arange(15)+.5

fig, ax = plt.subplots(figsize=(10,5))
fig = plt.barh(pos, x, align = 'center')
plt.yticks(pos, y)

plt.title("TOP 15 de autores con más publicaciones", fontsize=15)
plt.tick_params(direction='in', which='both', length=9, width=1, labelsize=12)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
plt.tight_layout()

plt.savefig("./figures/barh-authors.pdf")
plt.savefig("./figures/barh-authors.png")
plt.show()