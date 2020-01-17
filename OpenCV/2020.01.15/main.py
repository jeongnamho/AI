from flask import Flask, escape, request, send_file
import pprint
import urllib, cv2
import pytesseract
import numpy as np 
import matplotlib.pyplot as plt


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def imshow(tit, image):
    plt.title(tit)
    if len(image.shape) == 3:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else :
        plt.imshow(image, cmap='gray')
    plt.show()


app = Flask(__name__)

# set FLASK_APP=<파일명>.py
# flask run

@app.route('/tmp/<result>.png')
def img_file_download(result):
    file_name = f"tmp/"+result+".png"
    return send_file(file_name,
                    mimetype='image/png',
                    attachment_filename=result+'.png', # 다운받아지는 파일 이름.
                    as_attachment=True)

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
    img_blur = cv2.medianBlur(gray, 21)
    _, binary = cv2.threshold(img_blur, 80, 255, cv2.THRESH_BINARY)
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
    pts1 = np.float32([list(point_list[0]),
                    list(point_list[1]),
                    list(point_list[2]),
                    list(point_list[3])])
 
    # print(pts1)
    pts2 = np.float32([[0,0], [0,height], [width,height], [width,0]])
    # print(pts2)
    M = cv2.getPerspectiveTransform(pts1, pts2)
    # print(M)
    img_result = cv2.warpPerspective(img, M, (width, height))
    # _, binary = cv2.threshold(img_result, 230, 255, cv2.THRESH_BINARY)
    cv2.imwrite("namecard2.jpg", img_result)
    
    # imshow('', img_result)
    str = pytesseract.image_to_string(img_result, lang="eng+kor")
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

@app.route('/findbooks', methods=['POST'])
def findbooks():
    body = request.json
    pprint.pprint(body)
    image_url = body['action']['detailParams']['findbooks']['origin']

    urllib.request.urlretrieve(image_url, "./findbooks.jpg")

    print(image_url)
    with urllib.request.urlopen(image_url) as input:
        with open('./findbooks.jpg', 'wb') as output:
            output.write(input.read())

    image = cv2.imread("findbooks.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gassian_blur = cv2.GaussianBlur(gray, (3, 3), 0)
    # cv2.Canny(***, minVal, maxVal)
    # minVal보다 작으면 엣지 아니라고 판단
    # maxVal보다 크면 확실한 엣지
    # 그 사이는 판단함
    edged = cv2.Canny(gassian_blur, 10, 250) # Canny : 외곽선 정보를 알려주는 함수(edge 추출 방법)

    # imshow('gaussian_blur', edged)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    # imshow("", closed)
    # 여기서는 closed2으로 해봄
    cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0

    # cv2.drawContours(image, cnts, -1, (0,0,255), 1)
    # cv2.imwrite("output3.png")

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
            total += 1
    str = "I found {0} books in that image".format(total)
    # imshow("Output", image)
    print(str)
    return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": str
                }
            # {
            #     "simpleImage": {
            #         "imageUrl" : "http://b626c5f5.ngrok.io/tmp."+findbooks+".jpg",
            #         "altText" : 책
            #     }
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