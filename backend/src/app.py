from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/Investigacion2'
mongo = PyMongo(app)

db = mongo.db.departamentos


@app.route('/')
def index():
    return '<h1>Hello World</h1>'


if __name__ == "__main__":
    app.run(debug=True)

