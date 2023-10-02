import jwt
import datetime
from flask import Flask, request, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

app = Flask(__name__)

#Gets RSA Key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

#Creates the key identifier (kid)
kid = "key-id"

#Set the key's expiration time to 1 hour in the future
expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

#Endpoint to serve JWKS
@app.route('/jwks', methods=['GET'])
def jwks():
    if datetime.datetime.utcnow() < expiration_time:
        jwks = {
            "keys": [
                {
                    "kty": "RSA",
                    "kid": kid,
                    "use": "sig",
                    "n": public_key.public_numbers().n,
                    "e": public_key.public_numbers().e,
                }
            ]
        }
        return jsonify(jwks)
    else:
        return jsonify({"message": "Key expired"}), 400

#Endpoint to authenticate and issue JWTs
@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    #Tests the authentication of the given credentials
    if username == "userABC" and password == "password123":
        if datetime.datetime.utcnow() < expiration_time:
            payload = {
                "sub": username,
                "exp": expiration_time,
                "kid": kid
            }
            #If authentication is valid then token is returned and expiration status
            token = jwt.encode(payload, private_key, algorithm='RS256')
            return jsonify({"access_token": token})
    else:
        #If authentication failed then an failed message and error code 401 is returned
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(port=8080)
