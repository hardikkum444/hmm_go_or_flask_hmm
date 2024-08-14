# Adding new data to resource using put/post and adding the data in the body

from flask import Flask
from flask.json import jsonify
from flask_restful import Api, Resource
from flask_restful.reqparse import request
import requests

app = Flask(__name__)
api = Api(app)

videos = {

}

class Videos(Resource):
    def get(self, id):
        if id in videos:
            return jsonify(videos[id])
        return jsonify("No such video exists")

    def post(self, id):
        return jsonify(request.form['likes'])


api.add_resource(Videos, "/videos/<int:id>")

if __name__=="__main__":
    app.run(debug=True)

# This is how the request looks like

import requests

BASE = "http://127.0.0.1:5000/"

response1 = requests.post(BASE + "videos/1",{"name":"mandom","views":90,"likes":23})

print(response1.json())

