from flask import Flask, url_for
from my_app.movie import movie_bp
app = Flask(__name__)

app.register_blueprint(movie_bp)
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
