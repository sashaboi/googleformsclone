from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from gforms import views
urlpatterns = [
    path('',views.home , name='home'),
    path('allforms/',views.allforms , name='allforms'),
    path('formview/<str:pk>',views.formview , name='formview'),
    path('responses/<str:pk>',views.responses , name='responses'),
    path('api/', views.apiOverview, name="api-overview"),
    path('formlist/', views.formlist, name="formlist"),
    path('questionlist/', views.questionlist, name="questionlist"),
    path('questionlist/<str:pk>', views.questionlistdetail, name="questionlistdetail"),

]