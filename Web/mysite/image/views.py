from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.views.generic import View
# from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.forms import Form
# from django.forms import CharField, Textarea, ValidationError
# from django import forms
#from blog.forms import PostForm
from . import forms
# (from blog import forms라고 해도 됌. 같은 폴더에 있어서)
from . import models

"""
def list(request) :
    username = request.session["username"]
    user = User.objects.get(username=username)
    data = models.Post.objects.all().filter(author=user)
    context = {"data":data, "username":username}
    return render(request, "blog/list.html", context)

def detail(request, pk) :
    p = get_object_or_404(models.Post, pk=pk)
    return render(request, "blog/detail.html", {"d":p})
"""


class BoardView(View) :
    def get(self, request, pk, mode):
        # get 요청
        # 0/list -> 리스트 출력
        # 5/detail -> 5번 post를 보여줘
        # 0/add -> 신규 데이터 작성 -> post 발생
        # 5/edit -> 5번 post 수정
        if mode == "add" :
            form = forms.BoardForm()
        elif mode == "list" :
            username = request.session["username"]
            user = User.objects.get(username=username)
            data = models.Board.objects.all().filter(author=user)
            context = {"data": data, "username": username}
            return render(request, "myboard/list.html", context)
        elif mode == "detail" :
            p = get_object_or_404(models.Board, pk=pk)
            p.cnt += 1
            p.save()
            return render(request, "myboard/detail.html", {"d": p})
        elif mode == "edit" :
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(instance = post)
        else :
            return HttpResponse("error page")

        return render(request, "myboard/edit.html", {"form":form})


    def post(self, request, pk, mode):
        username = request.session["username"]
        user = User.objects.get(username=username)

        if pk == 0:
            form = forms.BoardForm(request.POST)
        else:
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            if pk == 0:
                post.author = user
            post.save()
            return redirect("myboard", 0, 'list')
        return render(request, "myboard/edit.html", {"form": form})


class LoginView(View) :
    def get(self, request):
        return render(request, "myboard/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user == None :
            return redirect("login")
        request.session["username"] = username
        return redirect("list")