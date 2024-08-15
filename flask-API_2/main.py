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

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"



video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the Video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views on the Video are required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the Video are required", required=True)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.get(video_id)
        return result

    def put(self, id):
        abort_if_exist(id)
        args = video_put_args.parse_args()
        videos[id] = args
        return videos[id], 201

    def delete(self, id):
        abort_if_not_exist(id)
        del videos[id]
        return "Deleted Successfuly", 204 # 204 -> deleted successfully

api.add_resource(Video,"/video/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
