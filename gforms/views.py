from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .forms import FormmainForm
from .models import FormMain , Question ,Answer, mcqchoice
import csv
import pandas as pd
from rest_framework import serializers, status
from .serializers import FormmainSerializer ,Questionserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def formlist(request):
    forms = FormMain.objects.all()
    serializer = FormmainSerializer(forms , many = True)
    return Response(serializer.data)

@api_view(['GET'])
def questionlist(request):
    questions = Question.objects.all()
    serializer = Questionserializer(questions , many = True)
    return Response(serializer.data)

@api_view(['GET'])
def questionlistdetail(request,pk):
    questions = Question.objects.get(id= pk)
    serializer = Questionserializer(questions )
    return Response(serializer.data)

@api_view(['GET'])
def apiOverview(request):
    
    return Response("API Base Point")


def home(request):

    form = FormmainForm()

    if request.method =="POST":
        form = FormmainForm(request.POST or None , request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.createdby = request.user
            obj.save()
            print('formsaved')
            data = FormMain.objects.get(usethisbool = False)
            with open(data.csvfile.path , 'r') as f:
                reader = csv.reader(f)
                print(reader)
                for i , row in enumerate(reader):
                    if i==0:
                        pass 
                        # skip the first title row
                    else:
                        title = row[0]
                        typeof = row[1]
                        options = row[2]
                        booli = row[3]
                        print(title, typeof, options, booli)
                        if booli == "TRUE":
                            booli = True
                        else:
                            booli = False
                        print('changed booli is ', booli)
                        ques = Question.objects.create( formid = data ,questiontext = title , questiontype = typeof , questionnumber = i , required = booli )
                        if typeof == "SingleSelect":
                            optionlist = options.split(",")
                            for opt in optionlist:
                                print(opt)
                                mcqchoice.objects.create(questionid = ques , choice = opt)
            data.usethisbool = True
            data.save()
        else:
            print(form.errors , 'form error')
        return render(request,'home.html')
    else:
        form = FormmainForm()

        context = {'form' : form}
        return render(request,'home.html',context)


def allforms(request):
    allforms = FormMain.objects.all()
    context = {'allforms':allforms}
    return render(request,'allforms.html',context)

def responses(request,pk):
    formidget = FormMain.objects.get(id=pk)
    questions = Question.objects.filter(formid = formidget)
    listofanswers =[]
    for i in questions:
        # find all answers related to all questions
        allanswers = Answer.objects.filter(questionid = i)
        for q in allanswers:
            listofanswers.append(q)
    print(listofanswers)    
    context = {'questions':questions , 'listofanswers': listofanswers}
    return render(request,'seeresponses.html',context)

def formview(request,pk):
    form = FormMain.objects.get(id=pk)
    questions = Question.objects.filter(formid = pk)
    for que in questions:
        if que.questiontype =="SingleSelect":

            mcqoptions = mcqchoice.objects.filter(questionid = que)
    print(questions[0])
    if request.method == "POST":
        for i in range(len(questions)):
            print(request.POST)
            # print('form submitted : ' , request.POST[questions[i].questiontext])
            questioninstance = Question.objects.get(id =questions[i].id )
            Answer.objects.create(userid = request.user , questionid = questioninstance , answerdata =request.POST[questions[i].questiontext] )
        context = {}
    else :
        context = {'form':form ,'questions':questions ,'mcqoptions':mcqoptions}
    return render(request,'formview.html',context)