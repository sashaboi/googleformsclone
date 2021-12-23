from os import name
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from gforms import views
urlpatterns = [
    path('',views.home , name='home'),
    path('allforms/',views.allforms , name='allforms'),
    path('formview/<str:pk>',views.formview , name='formview'),
    path('formedit/<str:pk>',views.formedit , name='formedit'),
    path('responses/<str:pk>',views.responses , name='responses'),
    path('api/', views.apiOverview, name="api-overview"),
    path('formlist/', views.formlist, name="formlist"),
    path('questionlist/<str:pk>', views.questionlist, name="questionlist"),
    path('questiondetail/<str:pk>', views.questionlistdetail, name="questionlistdetail"),
    path('loginonly', views.loginonly, name='loginonly'),
    path('formtakerapi', views.formtakerapi, name='formtakerapi'),
    path('showform/<str:pk>', views.showform, name='showform'),
    path('fillform/<str:pk>', views.fillform, name='fillform'),
    path('viewresponsesapi/<str:pk>', views.viewresponsesapi, name='viewresponsesapi'),
    path('userdataapi/<str:pk>', views.userdataapi, name='userdataapi'),
    path('changequestion/', views.changequestion, name='changequestion'),
    path('deletequestion/<str:pk>', views.deletequestion, name='deletequestion'),

]