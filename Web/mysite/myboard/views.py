from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import CharField, Textarea, ValidationError
from django import forms
#from blog.forms import PostForm  # 프로젝트 명이 바뀌면 blog를 바꿔야하므로 좋지 않음
from . import models
from . import forms
from . import apps
from django.core.paginator import Paginator

# url: bolg -> index함수 실행
def index(request):
    return HttpResponse('ok')

def page(request):
    datas = [{'id': 1, 'name':  '홍길동1'},
            {'id': 2, 'name':  '홍길동2'},
            {'id': 3, 'name':  '홍길동3'},
            {'id': 4, 'name':  '홍길동4'},
            {'id': 5, 'name':  '홍길동5'},
            {'id': 6, 'name':  '홍길동6'},
            {'id': 7, 'name':  '홍길동7'},
            ]

    page = request.GET.get('page', 1)  #default: 1
    p = Paginator(datas, 3)# collections 형태의 데이터,  # 한 페이지에 보여줄 데이터 개수
    sub = p.page(page) # 몇번째 페이지를 가지고 올 지 
                    # 슬라이싱의 개념과 같음

    return render(request, 'myboard/page.html', {'datas': sub})

def ajaxdel(request) :
    pk = request.GET.get("pk")
    board = models.Board.objects.get(pk=pk)
    board.delete()
    return JsonResponse({"error":'0'})

def ajaxget(request) :
    page = request.GET.get('page',1)

    datas = models.Board.objects.all().filter(category='common')
    
    
    page= int(page)
    subs= datas[(page-1)*3:(page)*3]
    
    """ 바로 위의 코드랑 똑같은 건데 url에서 page가 큰 수를 쓰더라도 오류가 나지 않고 빈 데이터로 나옴
    p = Paginator(datas, 3)
    subs = p.page(page)
    """
    
    datas = {'datas': [{"pk":data.pk, "title":data.title, "cnt":data.cnt} for data in subs]}
    return JsonResponse(datas, json_dumps_params = {"ensure_ascii":False} )


    # p = Paginator(datas, 3)
    # subs = p.page(page)



### <int:pk>/ <mode>를 url을 사용하기 위해
class BoardView(View) :
    def get(self, request, category, pk, mode):
        print(pk, mode)
        if mode =='add':
            # pk값은 상관없음.
            form = forms.BoardForm()
            return render(request, 'myboard/edit.html', {'form': form})
        elif mode == 'list':
            # pk값 상관없음.
            username = request.session.get('username', '')
            user = User.objects.get(username =username)
            data= models.Board.objects.all().filter(author = user, category = category)

            page = request.GET.get("page", 1)
            p = Paginator(data, 3)
            subs = p.page(page) # (page-1)*3 : page3
            context = {'datas': subs,'username': username, 'category': category}
            return render (request, apps.APP + '/list.html', context)

        elif mode =='detail':
            p = get_object_or_404(models.Board, pk = pk)
            # 조회수 증가
            p.cnt +=1
            p.save()
            return render(request,  apps.APP + '/detail.html', {'d': p, 'category': category})

        elif mode == 'edit':
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(instance=post)

        elif mode =='delete':
            post = get_object_or_404(models.Board, pk=pk)
            post.delete()
            return redirect(category +'/0/list')
        else:
            return HttpResponse('mode를 잘 입력하세용')
        return render(request, apps.APP +'/edit.html', {"form":form}) # 정확하게 입력



    def post(self, request, category, pk, mode):

        username = request.session["username"]
        user = User.objects.get(username=username)

        if pk == 0:
            form = forms.BoardForm(request.POST)
        else:
            # 바뀌기 전 데이터
            post = get_object_or_404(models.Board, pk=pk)
            # 바뀌기 전 데이터로부터 form을 생성
            form = forms.BoardForm(request.POST, instance=post)

        if form.is_valid():
            # 바뀐 데이터를 저장은 하지 말고 post에 갖고 오기
            post = form.save(commit=False)
            # add할 때 저장정보 넣고
            if pk == 0:
                post.author = user
                post.category = category
            post.save()
            return redirect("myboard", category, 0, 'list')  
        # return render(request, "myboard/edit.html", {"form": form})
        return render(request, apps.APP + '/edit.html', {"form": form})
            
          


