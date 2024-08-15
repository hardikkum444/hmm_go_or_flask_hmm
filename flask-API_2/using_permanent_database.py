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
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the Video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views on the Video are required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the Video are required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the Video is required")
video_update_args.add_argument("views", type=int, help="Views on the Video are required")
video_update_args.add_argument("likes", type=int, help="Likes on the Video are required")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields) # so that return thingy gets serialised
    def get(self, id):
        result = VideoModel.query.filter_by(id=id).first() # using filter by id and displying the 'first' result, you can also use 'all''
        if not result:
            abort(404,message="Video ID does not exist")
        return result

    @marshal_with(resource_fields) # so that return thingy gets serialised
    def put(self, id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=id).first() # to check if video already exists or not
        if result:
            abort(409, message="Video ID already exists")
        video = VideoModel(id = id, name = args['name'], views = args['views'], likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Video ID does not exist")

        if args['name']: # automatically checks if it aint none
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit() # no need of db.session.add when patching

        return result

    def delete(self, id):
        abort_if_not_exist(id)
        del videos[id]
        return "Deleted Successfuly", 204 # 204 -> deleted successfully

api.add_resource(Video,"/video/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
