from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
  return "Hello, World!"

@app.route('/sec')
def hello_world():
    my_secret = os.environ.get('MY_SECRET')
    return f'My secret is: {my_secret}'

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
