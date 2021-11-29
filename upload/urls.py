from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload-color/', views.upload_color, name='upload-color'),
]