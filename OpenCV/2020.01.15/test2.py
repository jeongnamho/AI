from flask import Flask, escape, request
import pickle
app = Flask(__name__)

# set FLASK_APP=<파일명>.py
# flask run
db = pickle.load('./db.bin')
id = 0
@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/users', methods=['POST'])
def create_user():
    global id
    body = request.json
    # print(body)
    body['id']=id
    # todo body에 id를 넣어준다.
    #db[str(id)]=body
    pickle.dump('./db.bin')
    id+=1
    return body

@app.route('/users/<id>', methods=['GET'])
def select_user():
    if id not in db:
        return {}, 404
    return db[id]

@app.route('/users/<id>', methods=['DELETE'])
def delete_user():
    del db[id]
    return {}

@app.route('/users/<id>', methods=['PUT'])
def update_user():
    pass



@app.route('/hi', methods=['POST'])
def hi():
    return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "간단한 텍스트 요소입니다."
                }
            }
        ]
    }
}