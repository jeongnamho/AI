from flask import Flask, request
import requests
import urllib
from bs4 import BeautifulSoup

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
    return "<font color=red>" + info["temp"] + "도 " + info["desc"] + "</font>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True) # 0.0.0.0은 누구나 다 들어올 수 있게 하려고