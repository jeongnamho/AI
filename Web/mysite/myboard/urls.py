from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('ajaxdel', views.ajaxdel),
    path('ajaxget', views.ajaxget),
    path('<category>/<int:pk>/<mode>/', views.BoardView.as_view(), name='myboard'),
    # path('', lambda request: redirect('myboard', 0, 'list')),
]