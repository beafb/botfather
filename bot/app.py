# coding:utf8
from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager
from functools import partial
import gevent
import sys
from datetime import datetime
from pprint import pprint


reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)

def get_movie(query, f):
    if f == "series":
        return 'https://fmovies.se/search?keyword=%s' % query
    else:
        html = requests.get('https://fmovies.se/search?keyword=%s' % query).content
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find('a', attrs={"class": u"poster"})
        lien = "https://fmovies.se/%s" % a["href"]
        print "lien == %s" % lien
        return lien


def do_work(f, result):
    film = requests.get('http://www.omdbapi.com/?i=%s&page=1' % result['imdbID']).json()
    if film["Poster"] != "N/A":
        print "f", f
        if "–" in film['Year']:
            film['Year'] = film['Year'].split("–")[0]
        movie = {
            "title": "%s" % film['Title'],
            "subtitle": "ratings : %s/10\nreleased : %s" % (film['imdbRating'], film['Year']),
            "image_url": film['Poster'],
            "buttons": [
                {
                    "type": "web_url",
                    "url": "http://www.imdb.com/title/%s/" % result['imdbID'],
                    "title": "Trailer"
                },
                {
                    "type": "web_url",
                    "url": get_movie(film['Title'], f),
                    "title": "Watch"
                },
                {
                    "type": "show_block",
                    "block_name": "choice",
                    "title": "Another %s" % f
                }
            ]
        }
        return movie


@app.route('/imdb', methods=['GET', 'POST'])
def get_kung():
    if request.method == 'GET':
        query = request.args.get("film")
        f = request.args.get("format")
        r = requests.get('http://www.omdbapi.com/?s=%s&page=1&type=%s' % (query, f))
        data = r.json()
        if data["Response"] == "False":
            if f == "movie":
                block = "film"
            else:
                block = "serie"
            message = {
                "messages": [
                    {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "button",
                                "text": "What the fuck did you type?",
                                "buttons": [
                                    {
                                        "type": "show_block",
                                        "block_name": block,
                                        "title": "retry"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://www.youtube.com/watch?v=Dd7FixvoKBw&start=63",
                                        "title": "Wanna go to war Belake?"
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
            return jsonify(message)
        messages = []
        func = partial(do_work, f)
        pool = Pool(9)
        results = []
        '''print "SEARCH", data['Search']
        for item in data['Search']:
            pool.apply_async(do_work, (f, item), callback=results.append)'''
        results = pool.map(func, data['Search'])
        pool.close()
        pool.join()
        '''jobs = [gevent.spawn(do_work, f, item) for item in data['Search']]
        gevent.wait(jobs)
        results = [job.value for job in jobs]'''
        results = [r for r in results if r is not None]
        print "RESULTS"
        pprint(results)
        if f == "movie":
            results = sorted(results, key=lambda rs: datetime.strptime(rs['subtitle'].split("released : ")[1], '%Y'), reverse=True)

        card = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": results
                }
            }
        }
        messages.append(card)
        print "MESSAGES", messages
        return jsonify(dict(messages=messages))
    else:
        return "c'est pas un film"

@app.route('/index')
def landing():
    lien = request.args.get("lien")
    lien = "https://fmovies.se/%s" % lien
    return render_template('index.html', lien=lien)


@app.route('/mee')
def mee():
    return render_template('bot.html')

if __name__ == "__main__":
    app.run(debug=True)
