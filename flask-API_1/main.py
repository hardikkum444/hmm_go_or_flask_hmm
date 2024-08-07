from flask import Flask, request, jsonify

app = Flask(__name__)

# Demostrating a Get request
@app.route("/get-user/<user_id>") # using a path parameter
def get_user(user_id):

    user_data = {
        "user_id": user_id,
        "name": "Banana Man",
        "email": "man.banana@gmail.com"
    }

    extra = request.args.get("extra")

    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

# Demonstrating a POST request
@app.route("/create-user", methods=["POST"])
def create_user():

    # if request.method == "POST" To check if we have multiple req types in "methods"

    data = request.get_json()
    data["verified?"] = "YES"

    return jsonify(data), 201



if __name__ == "__main__":
    app.run(debug=True)
