## Web Scraping en el Journal of Macroeconomics
# El objetivo es vincularme con la p�gina web del Journal of Macroeconomics para extraer la
# informacion de cada volumen, los articulos de cada uno, los autores, los links, entre otros.
# Voy a trabajar con un entorno virtual llamado `env`. El Driver de Chrome se puede descargar
# en https://sites.google.com/chromium.org/driver/downloads


import pandas as pd
import utils

import warnings
warnings.simplefilter("ignore")


## Vinculaci�n al Journal of Macroeconomics y obtenci�n de HTML ===============
url_1 = "https://www.sciencedirect.com/journal/journal-of-macroeconomics/issues?page=1"
url_2 = "https://www.sciencedirect.com/journal/journal-of-macroeconomics/issues?page=2"
url_3 = "https://www.sciencedirect.com/journal/journal-of-macroeconomics/issues?page=3"
page_1 = utils.get_html(url_1)
page_2 = utils.get_html(url_2)
page_3 = utils.get_html(url_3) # time: 2 minutos

## Extracci�n de HTML a informaci�n de vol�menes ==============================
names_1, urls_1, dates_1 = utils.get_volumens(page_1)
names_2, urls_2, dates_2 = utils.get_volumens(page_2)
names_3, urls_3, dates_3 = utils.get_volumens(page_3)

names = names_1 + names_2 + names_3
urls = urls_1 + urls_2 + urls_3
dates = dates_1 + dates_2 + dates_3

dta_volumens = pd.DataFrame({
    "volume_name": names,
    "volume_date": dates,
    "volume_url": urls
})


## Obtenci�n de art�culos en cada volumen =====================================
urls = dta_volumens["volume_url"] # time: 50 minutos
articles = utils.get_articles(urls)

dta_articles = pd.DataFrame(
    articles, columns=["volume_url", "article_name", "article_url"]
)

## Obtenci�n de informaci�n de cada uno de los art�culos ======================
urls = dta_articles["article_url"]  # time: 18 horas
components = utils.get_components(urls)

dta_components = pd.DataFrame(
    components, columns=["article_url", "authors", "doi"]
)


## Modificaci�n final de los datos ============================================
dta = dta_components.merge(dta_articles, how="inner").merge(dta_volumens, how="inner")

dta["article_url"] = "https://www.sciencedirect.com" + dta["article_url"].astype(str)
dta["volume_url"] = "https://www.sciencedirect.com" + dta["volume_url"].astype(str)

dta_f = dta[["article_name", "authors", "article_url", "doi", "volume_name",
             "volume_date", "volume_url"]]
dta_f[0:10]


## Guardado
dta_f.to_pickle("./data/dta.pkl")
dta_f.to_csv("./data/dta.csv", sep=';')
