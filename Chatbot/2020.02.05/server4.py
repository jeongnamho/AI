from flask import Flask, request, jsonify
import requests
import urllib
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


# 얘는 dictionary 형태로 리턴받음
def getWeather2(city):
    url = 'https://search.naver.com/search.naver?query='
    url = url + urllib.parse.quote_plus(city + "날씨")
    print(url)
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    temp = bs.select('span.todaytemp')
    desc = bs.select('p.cast_txt')
    return {"temp":temp[0].text, "desc":desc[0].text}


@app.route("/")
def home():
    name = request.args.get("name")    # 크롬의 URL창에서 127.0.0.1:5020/?name=abc 라고 치면 결과값 보임
    item = request.args.get("item")
    return "hello~~" + name + item

@app.route("/abc")
def abc():
    return "test"

@app.route('/weather')
def weather():
    city = request.args.get("city")
    info = getWeather2(city)
#     return json.dumps(info)
    return jsonify(info) # 위랑 똑같음

@app.route('/dialogflow', methods=['POST', 'GET'])  # 웹브라우저에서는 GET방식만 보이기 때문에 웹에서 보려면 GET방식을 꼭 넣어야함
def dialogflow():
    res = {'fulfillmentText': 'Hello~~~~'}
    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True) # 0.0.0.0은 누구나 다 들어올 수 있게 하려고
