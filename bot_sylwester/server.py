from flask import Flask
from flask_restful import Api, Resource, reqparse


def run_server(port):
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Wish, "/message/wish")
    api.add_resource(Emoji, "/message/emoji")
    api.add_resource(Fireworks, "/message/fireworks")
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)


class Wish(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("value")
        parser.add_argument("author")
        args = parser.parse_args()
        print(args)
        return {"args": args}


class Emoji(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("emoji")
        parser.add_argument("emojiURL")
        parser.add_argument("author")
        args = parser.parse_args()
        print(args)
        return {"args": args}


class Fireworks(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("effect")
        parser.add_argument("parameters")
        args = parser.parse_args()
        print(args)
        return {"args": args}
