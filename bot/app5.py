import requests
from bs4 import BeautifulSoup
import time
from multiprocessing.dummy import Pool as ThreadPool


def do_work(item):
    url = 'https://fmovies.se/'
    r = requests.get("%s/%s" % (url, item['data-tip'])).content
    soup2 = BeautifulSoup(r, 'html.parser')
    title = soup2.find('h1')
    h1 = title.text
    quality = soup2.find('span', attrs={"class": u"quality"}).text
    ratings = soup2.find('span', attrs={"class": u"imdb"}).text
    duration = soup2.find('span', attrs={"class": u"duration"}).text
    desc = soup2.find('p', attrs={"class": u"desc"}).text
    labels = soup2.findAll('label')
    countries = []
    genre = []
    release = None
    stars = None
    url = soup2.find("a", attrs={"class": "watch-now"})["href"]
    for label in labels:
        if label.text == "Country:":
            for c in label.next_siblings:
                if c.name == "a":
                    countries.append(c.text)
        elif label.text == "Genre:":
            for c in label.next_siblings:
                if c.name == "a":
                    genre.append(c.text)
        elif label.text == "Stars:":
            stars = label.parent.text.split(':')[1]
    if "?" in ratings:
        ratings = None
    else:
        ratings = float(ratings.replace("IMDb ", ""))
    titlediv = soup2.find("div", attrs={"class": "title"})
    children = titlediv.findChildren()
    for child in children:
        if child.name == "span":
            release = int(child.text)
    data = requests.get("http://www.omdbapi.com/?apikey=5820a653&t=%s&y=%s&type=movie" % (h1, release)).json()
    if data['Response'] != "False":
        if data['Poster'] != "N/A":
            img = data['Poster']
        else:
            img = "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-9/18034310_226695687812115_2221376000230612564_n.jpg?oh=2d00ddef24aa626802f7499ccad2590c&oe=598AF840"
    else:
        img = "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-9/18034310_226695687812115_2221376000230612564_n.jpg?oh=2d00ddef24aa626802f7499ccad2590c&oe=598AF840"
    obj = {
        "title": h1,
        "quality": quality,
        "ratings": ratings,
        "duration": duration,
        "description": desc,
        #"countries": countries,
        #"genre": genre,
        "stars": stars,
        "url": url,
        "release": release,
        "img": img
    }
    print obj
    url = "http://127.0.0.1:8000/api/film"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "1b0e475a-4bb1-5ad9-54cb-f6a20dea34ef"
    }

    response = requests.request("POST", url, json=obj, headers=headers)
    return response.json()


results = []
for page in range(1, 440):
    pool = ThreadPool(100)
    html = requests.get('https://fmovies.se/movies?page=%s' % page).content
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', attrs={"class": u"item"})
    results = pool.map(do_work, items)
    pool.close()
    pool.join()
    time.sleep(0.9)
    page += 1
print "cacas"
