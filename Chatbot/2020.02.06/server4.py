from flask import Flask, request, jsonify
import requests
import urllib
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



# 얘는 dictionary 형태로 리턴받음
def getWeather2(city):
    url = 'https://search.naver.com/search.naver?query='
    url = url + urllib.parse.quote_plus(city + "날씨")
    print(url)
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    temp = bs.select('span.todaytemp')
    desc = bs.select('p.cast_txt')
    return {"temp":temp[0].text, "desc":desc[0].text}

def getQuery(word, k) : # 네이버 지식백과에서 k번째 정의 가져오기 함수
    url = 'https://search.naver.com/search.naver?where=kdic&query='
    url = url + urllib.parse.quote_plus(word)
    print(url)
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    output = bs.select('p.txt_box')
    return output[k-1].text

def processdialog(req):
    answer = req['queryResult']['fulfillmentText']
    intentName = req['queryResult']['intent']['displayName']
    
    if intentName == "query" :
        word = req["queryResult"]["parameters"]["any"]
        text = getQuery(word,1)
        res = {'fulfillmentText':text}
    elif intentName == "weather":
        date = req['queryResult']['parameters']['date']
        geo_city = req['queryResult']['parameters']['geo-city']
        info = getWeather2(geo_city)
        res = {"fulfillment": f"{geo_city} 날씨 정보 : {info['temp']} / {info['desc']}" }
    else:
        res = {'fulfillmentText' : answer}
    
    return res



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
def dialogflow():                                  # 하지만 dialogflow는 무조건 post방식임! 그래서 post방식도 함께 써줘야 한다.
    if request.method =='GET' :
        file = request.args.get("file")
        with open(file, encoding='UTF8') as json_file:
            req = json.load(json_file)
            print(json.dumps(req, indent=4, ensure_ascii=False)) # 한글 안깨지게
    else:
        req = request.get_json(force=True)
        print(json.dumps(req, indent=4, ensure_ascii=False)) # 한글 안깨지게
        
    return jsonify( processdialog(req) )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True) # 0.0.0.0은 누구나 다 들어올 수 있게 하려고
