import feedparser
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['HOST'] = '127.0.0.1'
app.config['PORT'] = '5000'

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
def index():
  return redirect('http://flask.rawfactor.net/bbc', code=302)

@app.route("/<publication>")
def get_news(publication):
  feed = feedparser.parse(RSS_FEEDS[publication])
  return render_template("home.html", articles=feed['entries'])

if __name__ == '__main__':
  app.run()