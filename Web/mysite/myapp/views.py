from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import face
from myapp.models import User

def index(request):
    return HttpResponse("Hello DJango!!!")


def test(request):
    data = {"message":"안녕", "s":{"img":"test.png"}, "list":[1,2,3,4,5]}
    return render(request,  # 변수명 관심 꺼도 됌
                  'template.html',  # 오픈할 템플릿 파일
                  data # templates.html로부터 'message' 대신 '안녕'을, 's.img'대신 'test.png'를 대입하겠다.
                  )


def login(request):
    id = request.GET["id"]
    pwd = request.GET["pwd"]
    if id == pwd :
        request.session["user"] = id
        return HttpResponse("login 성공~~~~ <a href=/service> 서비스로 </a>")
        # return redirect("/service")
        # 위의 return 대신에 return redirect("/service")를 쓰면 저절로 /service페이지로 넘어감
    return HttpResponse("login fail~~~~<a href=static/login.html> 로그인페이지로 </a>")

def logout(request):
    request.session["user"] = ""
    # request.session.pop("user")
    return redirect("/static/login.html")



def service(req) :
    if req.session.get("user", "") == "":
        return redirect("/static/login.html")
    html = "Main Service<br>" + \
           req.session.get("user") + \
           "님 감사합니다<a href=/logout>logout</a>"
    return HttpResponse(html)


@csrf_exempt  # 이건 걍 anotation
def uploadimage(request):
    file = request.FILES['file1']
    filename = file._name
    fp = open(settings.BASE_DIR + "/static/" + filename, "wb")
    for chunk in file.chunks():
        fp.write(chunk)
    fp.close()

    result = face.facerecognition(settings.BASE_DIR + "/known.bin", settings.BASE_DIR + "/static/" + filename)
    print(result)
    if result != "":
        request.session["user"] = result[0]
        return redirect("/service")
    return redirect("/static/login.html")



def listUser(request) :

    if request.method == "GET" :
        userid = request.GET.get("userid","")
        if userid != "":  # userid가 아무것도 없는 것을 삭제할 수 없으니까
            User.objects.all().get(userid=userid).delete()
            return redirect("/listuser")

        q = request.GET.get("q", "")
        data = User.objects.all()
        if q != "":
            data = data.filter(name__contains=q)
        return render(request, 'template2.html', {"data": data})
    else :
        userid = request.POST["userid"] #request.POST.get("userid")를 써도 됌!
        name = request.POST["name"]
        age = request.POST['age']
        hobby = request.POST["hobby"]


        # u = User(userid=userid, name=name, age=age, hobby=hobby).save()
        User.objects.create(userid=userid, name=name, age=age, hobby=hobby)  #이렇게 하면 굳이 윗 줄처럼 수정이 필요없다. 저절로 save가 되니까!

        return redirect("/listuser")







