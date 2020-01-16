from flask import Flask, escape, request
import pprint
import urllib, cv2
import pytesseract
import numpy as np 

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'




app = Flask(__name__)

# set FLASK_APP=<파일명>.py
# flask run
@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


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

@app.route('/namecard', methods=['POST'])
def namecard():
    body = request.json
    pprint.pprint(body)
    image_url = body['action']['detailParams']['namecard']['origin']

    urllib.request.urlretrieve(image_url, "./namecard.jpg")

    print(image_url)
    with urllib.request.urlopen(image_url) as input:
        with open('./namecard.jpg', 'wb') as output:
            output.write(input.read())

    img = cv2.imread('namecard.jpg')
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(gray, (9,9), 0)
    _, binary = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((3,3), np.uint8)
 
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=7)
 
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #RETR_EXTERNAL:외곽만
 
    # print(len(contours))
 
    length = cv2.arcLength(contours[0], True)  #도형 윤곽 길이, 폐곡선 여부 True
    approx = cv2.approxPolyDP(contours[0], 0.02 * length, True) #얼마나 꺾이는지 확인, 꼭지점 위치
    cv2.drawContours(img_copy, [approx], -1, (0,255,0),5)
 
    # imshow('', img_blur)
    # imshow('', binary)
    # imshow('', opening)
    # imshow('', img_copy)
 
    height, width = img.shape[:2]
    point_list = approx
    pts1 = np.float32([list(point_list[1]),
                    list(point_list[0]),
                    list(point_list[2]),
                    list(point_list[3])])
 
    # print(pts1)
    pts2 = np.float32([[0,0], [width,0], [0,height], [width,height]])
    # print(pts2)
    M = cv2.getPerspectiveTransform(pts1, pts2)
    # print(M)
    img_result = cv2.warpPerspective(img, M, (width, height))
    # imshow('', img_result)
    str = pytesseract.image_to_string(img_result)
    print(str)
    return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": str
                }
            }
        ]
    }
}


# def ocr(file):
#     # todo 명함정보 추출
#     img = cv2.imread('../2020.01.09/namecard.png')

# height, width = img.shape[:2]

# # 좌표순서 : 상단 왼쪽 끝, 상단 오른쪽 끝, 하단 왼쪽 끝, 하단 오른쪽 끝
# point_list = [[27, 179], [611,36], [118, 534], [754,325]]

# pts1 = np.float32([list(point_list[0]),
#                   list(point_list[1]),
#                   list(point_list[2]),
#                   list(point_list[3])])
# print(pts1)