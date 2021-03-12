from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)


@app.route('/')
def home():
    return {'status': 'ok'}


if __name__ == '__main__':
    app.run(debug=True)
