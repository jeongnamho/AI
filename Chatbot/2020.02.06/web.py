from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "hello~~"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True) # 0.0.0.0은 누구나 다 들어올 수 있게 하려고
