from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = "mandom"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':'token is missing'}), 403
        try:
            data = jwt.decode(token , app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message':'token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/unprotected', methods=['GET'])
def unprotected():
    return jsonify({'message':"You are accessing the unprotected data"}), 201

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message':"You are now accessing the protected data"}), 201

@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization

    if auth and auth.password == 'admin':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({"token" : token})
    return make_response("Could not verify!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == "__main__":
    app.run(debug=True)
