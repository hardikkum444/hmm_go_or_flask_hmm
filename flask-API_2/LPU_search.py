from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
import json


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

users = {
    "admin": "admin"
}

@auth.verify_password
def verify_pass(username, password):
    if username in users and users[username] == password:
        return username
    return None

class search_name(Resource):
    @auth.login_required
    def get(self, name):
        with open('output.json') as json_file:
            students = json.load(json_file)

        for student in students:
            if student["StudentName"].lower() == name.lower():
                return jsonify(student)

        return {"message": "Student not found"}

class search_regno(Resource):
    @auth.login_required
    def get(self, regno):
        with open ("output.json") as json_file:
            students = json.load(json_file)

        for student in students:
            if student["Reg_Number"] == regno:
                return jsonify(student)

        return {"message": "Student not found"}


api.add_resource(search_name, "/search_name/<string:name>")
api.add_resource(search_regno, "/search_regno/<int:regno>")

if __name__ == "__main__":
    app.run(debug=True)
