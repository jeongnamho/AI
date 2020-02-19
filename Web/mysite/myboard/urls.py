from django.urls import path
from . import views

urlpatterns = [
    path('<category>/<int:pk>/<mode>/', views.BoardView.as_view(), name='myboard'),
    path('', lambda request: redirect('myboard', 'common', 0, 'list')),
]