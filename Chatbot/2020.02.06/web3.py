from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home(): # 미리 static폴더를 web2.py파일이 있는 폴더에 하나 더 만들어놓고 Lena.png파일을 넣어놓고 해야함
    html = """
    <h1>hello</h1>
    <img src=/static/Lena.png> <br>   
    <iframe
    allow="microphone;"
    width="400"
    height="550"
    src="https://console.dialogflow.com/api-client/demo/embedded/namho">
</iframe>
    """
    return html

cnt=0
@app.route('/counter')
def counter():  # 두가지 방법이 있음
    global cnt
    cnt += 1
    """
    html = ""
    for i in str(cnt) :
        html +=f"<img src=/static/{i}.png width=32>"
    html += "명이 방문했습니다."
    """
    html = "".join([ f"<img src=/static/{i}.png width=32>" for i in str(cnt) ])
    html += "명이 방문했습니다."
    return html


@app.route('/weather', methods=["POST", "GET"])
def weather():
    if request.method == "GET" :
        req = request.args
    else : 
        req = request.form
    
    city = req.get("city")
    return f"{city} 날씨 좋아요"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True) # 0.0.0.0은 누구나 다 들어올 수 있게 하려고
