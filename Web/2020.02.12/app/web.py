from flask import Flask, render_template, request
import yolo


app=Flask(__name__)

listData = [
    {"id": 0, "img": "1.jpg", "title": "Meteor"},
    {"id": 1, "img": "2.jpg", "title": "삿포로"},
    {"id": 2, "img": "3.jpg?8", "title": "아이슬란드 야경"},
]


@app.route('/')
def index():
    return render_template('home.html', title='my home page')

@app.route('/image')
def image():
    return render_template('image.html', listData=listData )

@app.route('/view')   # /view?id=0>
def view():
    id = request.args.get("id")
    return render_template('view.html', s=listData[int(id)])

def goURL(msg, url):
    html = """
    <script>
        alert("@msg")
        window.location.href = "@url"
    </script>
        """
    html = html.replace("@msg", msg)
    html = html.replace("@url", url)
    return html


@app.route('/fileUpload', methods= ['POST'])
def fileUpload():
    f= request.files['file1']

    f.save("./static/" + f.filename)
    title = request.form.get("title")
    id = listData[len(listData)-1]["id"]+1
    yolo.detectObject("./static/" + f.filename)
    listData.append({"id": id, "img": f.filename, "title": title})
    return goURL("업로드가 성공했습니다.", "/image")

@app.route('/deleteimage') # /delete?id=0
def deleteimage():
    idx = -1
    id = int(request.args.get("id"))
    for i in range(len(listData)):
        if id == listData[i]["id"] :
            idx = i
    if idx >= 0 : del listData[idx]

    return goURL("자료를 삭제했습니다.", "/image")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)