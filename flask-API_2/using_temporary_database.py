from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

video = {

}

parsed_video = reqparse.RequestParser()
parsed_video.add_argument("name", help="Please give name of the video", required=True)
parsed_video.add_argument("likes", help="Please give likes on the video", required=True)
parsed_video.add_argument("views", help="Please give views on the video", required=True)


def abort_if_found(id):
    if id in video:
        abort(404, message="video ID already exists")

def abort_if_not_found(id):
    if id not in video:
        abort(404, message="video ID does not exist")

class Video(Resource):

    def get(self, id):
        abort_if_not_found(id)
        return video[id]

    def put(self, id):
        abort_if_found(id)
        args = parsed_video.parse_args()
        video[id] = args
        return "done", 201

    def delete(self, id):
        abort_if_not_found(id)
        del video[id]
        return "deletion completed", 204

api.add_resource(Video, "/video/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
