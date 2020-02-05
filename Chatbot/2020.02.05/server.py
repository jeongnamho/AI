from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    name = request.args.get("name")    # 크롬의 URL창에서 127.0.0.1:5020/?name=abc 라고 치면 결과값 보임
    item = request.args.get("item")
    return "hello~~" + name + item

@app.route("/abc")
def abc():
    return "test"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True) # 0.0.0.0은 누구나 다 들어올 수 있게 하려고