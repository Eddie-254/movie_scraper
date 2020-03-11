import urllib.request
from urllib.request import urlopen as uReq
import bs4
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np

#headers = {"Accept-Language": "en-US, en;q=0.5"}
my_url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"

uClient = uReq(my_url)
kurasa = uClient.read()
uClient.close()
page = soup(kurasa, "html.parser")
containers = page.findAll("div", {"class":"lister-item mode-advanced"})

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []


for container in containers:
 
 name = container.h3.a.text
 titles.append(name)

 year = container.h3.find("span", {"class":"lister-item-year"}).text
 years.append(year)

 runtime = container.find("span", {"class":"runtime"}).text if container.p.find("span", {"class":"runtime"}) else "-"
 time.append(runtime)

 imdb = float(container.strong.text)
 imdb_ratings.append(imdb)

 m_score = container.find("span", {"class":"metascore"}).text if container.find("span", {"class":"metascore"}) else "-"
 metascores.append(m_score)

 nv = container.findAll("span", attrs={"name":"nv"})

 vote = nv[0].text
 votes.append(vote)

 grosses = nv[1].text if len(nv) > 1 else "-"
 us_gross.append(grosses)


movies = pd.DataFrame({
    'movie' : titles,
    'year': years,
    'timeMin': time,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,
})


#print(titles)
#print(years)
#print(time)
#print(imdb_ratings)
#print(metascores)
#print(votes)
#print(us_gross)

movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))

movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')

movies.to_csv('movies.csv')

