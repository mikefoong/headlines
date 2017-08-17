from flask import Flask

app = Flask(__name__)

app.config['debug'] = True
app.config['host'] = '127.0.0.1'
app.config['port'] = '5000'

@app.route("/")
def get_news():
  return "no news is good news"

if __name__ == '__main__':
  app.run()