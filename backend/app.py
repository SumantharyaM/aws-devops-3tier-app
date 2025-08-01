from flask import Flask, jsonify
from flask_cors import CORS
from dynamo_client import get_items

app = Flask(__name__)

# ✅ Fully allow CORS from any origin for testing (TEMPORARY)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Backend API!'})

@app.route('/data')
def data():
    return jsonify(get_items())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
