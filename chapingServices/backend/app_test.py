# from flask import Flask


# app = Flask(__name__)


# @app.route("/hello")
# def hello():
#     return "Hello World!"


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='give a name')  

    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = self.parser.parse_args()
        for k, v in args.items():
            print(k, v)

        return args


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)