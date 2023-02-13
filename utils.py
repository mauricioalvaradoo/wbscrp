from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep



def get_html(url):

    """"" Vinculacion con la seccion de articulos del sitio web

    Parametros
    ----------
    url: link
        Link de la pagina web


    Retorno
    ----------
    soup: html
        Contenido de todo el html de la pagina web

    """""

    driver = webdriver.Chrome("./driver/chromedriver.exe")
    driver.get(url)

    # Clicks a los botones
    for i in range(1, 30):
        try:
            button = driver.find_element(By.XPATH, value=f'/html/body/div[3]/div/div/div/main/div[2]/div/section[2]/div/div/ol/li[{i}]/button')
            button.click()
            sleep(1)
        except:
            pass

    # Código fuente como HTML
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    driver.close()

    return soup




def get_volumens(soup):
    
    """"" Conseguir volumenes dentro de los links
    Clases
    -------  
    Secciones: `li`, `accordion-panel js-accordion-panel`
    Volumenes: `div`, `class="issue-item u-margin-s-bottom`
    Nombre del volumen: `span`, `anchor-text`
    Link: `a`, `js-issue-item-link text-m anchor-default`


    Parametros
    ----------
    soup: html
        Contenido de todo el html de la pagina web
    
    
    Retorno
    -------
    list_names: list
        Lista de los nombres de los volumenes
    list_urls: list
        Lista de los urls de los volumenes
    list_date: list
        Lista de las fechas de publicacion de los volumenes

    """""
    
    
    sections = soup.find_all("li", {"class": "accordion-panel js-accordion-panel"})

    list_names=[]
    list_urls=[]
    list_date=[]

    for section in sections:
        volumens = section.find_all("div", {"class": "issue-item u-margin-s-bottom"})

        for volume in volumens:
            name = volume.find("span", {"class": "anchor-text"}).text
            url = volume.find("a", {"class": "anchor js-issue-item-link text-m anchor-default"}).get("href")
            date = volume.find("h3", {"class": "js-issue-status text-s"}).text

            # Guardando los resultados
            list_names.append(name)
            list_urls.append(url)
            list_date.append(date)

    return list_names, list_urls, list_date




def get_articles(urls):
    
    """"" Conseguir los articulos dentro de los volumenes

    Clases
    -------
    Article: `h3`, `text-m u-font-serif u-display-inline`
    Url: `a`, `anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default`
    Name: `span`, `js-article-title`


    Parametros
    ----------
    urls: pd.Series
        Lista de urls de cada articulo


    Retorno
    -------
    list_articles: list
        Lista con tres elementos: url de volumen, nombre de articulo y url de articulo

    """""
    
    list_articles = []

    for i in urls:
        # Extraendo los nombres de los articulos en cada HTML
        soup = get_html(f"https://www.sciencedirect.com{i}")
        articles = soup.find_all("h3", {"class": "text-m u-font-serif u-display-inline"})

        for article in articles:
            name = article.find("span", {"class": "js-article-title"}).text
            url = article.find("a", {"class": "anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default"}).get("href")
            
            # Guardando resultados
            list_articles.append([i, name, url])    

    return list_articles




def get_components(urls):
    
    """""
    Clases
    ------
    Autores: `a`, `author size-m workspace-trigger`
    Nombre: `span`, `text given-name`
    Apellido: `span`, `text surname`
    Doi: `a`, `doi`
    

    Parametros
    ----------
    urls: pd.Series
        Lista de urls de cada articulo
    

    Retorno
    -------
    list_components: list
        Lista con cuatro elementos: url de articulo, nombres de autores, codigo doi

    """""

    list_components = []

    for i in urls:
        # Entraendo los componentes de cada uno de los articulos
        soup = get_html(f"https://www.sciencedirect.com{i}")


        try:
            # Elementos
            doi = soup.find("a", {"class": "doi"}).get("href")
            group_authors = soup.find_all("button", {"class": "button-link workspace-trigger button-link-primary"})

            list_authors = []

            for authors in group_authors:
                name = authors.find("span", {"class": "given-name"}).text
                surname = authors.find("span", {"class": "text surname"}).text

                author = f"{surname}, {name}"
                list_authors.append(author)

            # Union
            list_components.append([i, list_authors, doi])
        except:
            pass

    return list_components