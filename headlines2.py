import feedparser
from flask import Flask, render_template, request
import json
import urllib
#import urllib2

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['HOST'] = '127.0.0.1'
app.config['PORT'] = '5000'

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'bbc',
	    'city': 'Singapore, SG',
	    'currency_from': 'SGD',
	    'currency_to': 'USD'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ee6193d8cde9cf17a87449ebdb65dfb1"
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?app_id=4baf634e4b06493482d61828cc7436be"

@app.route("/")
def home():
    # Check for publications from user input or use the Default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
  
    # Check for weather city from user input or use the Default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
  
    # Check for currency from user input or use the Default
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']

    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rates(currency_from, currency_to)
    return render_template('home.html', articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate)
 
def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']
  
def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url)
    weather_data = data.read().decode('utf-8')
    parsed = json.loads(weather_data)
    weather = None
    if parsed.get('weather'):
        weather = {'description':parsed['weather'][0]['description'],
		   'tempreature':parsed['main']['temp'],
	       	   'city':parsed['name'],
	           'country':parsed['sys']['country']}
  
    return weather

def get_rates(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read().decode('utf-8')
  
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return float(to_rate/frm_rate)
    # return to_rate
  
if __name__ == '__main__':
    app.run()
