# from flask import Flask
# from flask_restful import Api, Resource

# app = Flask(__name__)
# api = Api(app)

# names = {
#     "John":{"age":20, "gender":"male"},
#     "Garreth":{"age":21, "gender":"male"},
#     "Linda":{"age":19, "gender":"female"}
# }

# class HelloWorld(Resource):

#     def get(self, name):
#         # return {"data": name,
#         # "age": age
#         # }

#         return names[name]

# api.add_resource(HelloWorld,"/helloworld/<string:name>")

# if __name__ == "__main__":
#     app.run(debug=True)

#-------------------------------------------------------------------

# Its important to set headers as key-> content-type value-> application/json
# For doing that make sure the payload you are sending via postman is in json format
# curl req should look like -> curl -X PUT -H "Content-Type: application/json" -d '{"name": "Sample Video", "views": 1234, "likes": 567}' http://localhost:5000/video/1

from flask.json import jsonify
from typing_extensions import Required
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the Video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views on the Video are required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the Video are required", required=True)

videos = {
}

def abort_if_not_exist(id):
    if id not in videos:
        abort(404, message="Video ID does not exist")

def abort_if_exist(id):
    if id in videos:
        abort(409, message="Video ID already exists")

class Video(Resource):

    def get(self, id):
        abort_if_not_exist(id)
        return videos[id]

    def put(self, id):
        abort_if_exist(id)
        args = video_put_args.parse_args()
        videos[id] = args
        return videos[id], 201

    def delete(self, id):
        abort_if_not_exist(id)
        del videos[id]
        return "Deleted Successfuly", 204 #204->deleted successfully

api.add_resource(Video,"/video/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
