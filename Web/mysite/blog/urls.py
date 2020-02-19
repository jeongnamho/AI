from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index),
    # path('<name>/', views.index2),    # <name>은 parameter를 의미함
    # path('<int:pk>/detail', views.index3),    # pk가 정수값으로 주어진다고 가정
    # path('list/', views.list, name='list'),
    # path('<int:pk>/detail/', views.detail, name='detail'),
    # path('list2', views.PostView.as_view()),
    path('login/', views.LoginView.as_view(), name="login"),
    # path('add/', views.PostView.as_view(), name='add'),
    # path('<int:pk>/edit/', views.PostEditView.as_view(), name='edit'),
    path('<int:pk>/<mode>/', views.PostEditView.as_view(), name='edit'),
]