from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .forms import FormmainForm
from .models import FormMain , Question ,Answer, mcqchoice
import csv
import pandas as pd
from rest_framework import serializers, status
from .serializers import FormmainSerializer ,answerserializer,Questionserializer,Allserializer ,mcqchoiceserializer, userserializer
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User



#return user's email and username for ID
@api_view(['GET'])
def userdataapi(request,pk):
    user = User.objects.get(id=pk)
    serializer = userserializer(user )
    return Response(serializer.data)



# Fill form api data : this api takes in the formid, and gives the form name, the questions in the form, and any mcq options (if available)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showform(request,pk):
    boolformcq = False
    form = FormMain.objects.get(id=pk)
    formforapi =FormMain.objects.filter(id=pk)
    questions = Question.objects.filter(formid = pk)
    for que in questions:
        if que.questiontype =="SingleSelect":
            boolformcq = True
            mcqoptions = mcqchoice.objects.filter(questionid = que)
    formdata = FormmainSerializer(formforapi,many = True)
    questionsdata = Questionserializer(questions,many = True)
    if boolformcq == True:
        mcqdata = mcqchoiceserializer(mcqoptions,many = True)
        finaldata = formdata.data + questionsdata.data + mcqdata.data
    else:
        finaldata = formdata.data + questionsdata.data
    return Response(finaldata)

#return question individual from ID
@api_view(['GET'])
def deletequestion(request,pk):
    Question.objects.get(id=pk).delete()
    
    return Response("done")

#this api edits questions when a question json is submitted
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changequestion(request):
    question = Question.objects.get(id=request.data['id'])
    question.questiontext = request.data['questiontext']
    question.questiontype = request.data['questiontype']
    question.required = request.data['required']
    question.save()
    newquestion = Question.objects.get(id=request.data['id'])
    print('requestdata: ', request.data ,  'new question object: ', newquestion)
    return Response("done")

#this api fills the forms. it takes answer json and creates answer object. 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fillform(request,pk):
    # serializer = answerserializer(data = request.data)
    print(request.data)
    questions = Question.objects.filter(formid = pk)
    for i in range(len(questions)):
            print(request.data)
            # print('form submitted : ' , request.POST[questions[i].questiontext])
            questioninstance = Question.objects.get(id =questions[i].id )
            Answer.objects.create(userid = request.user , questionid = questioninstance , answerdata =request.POST[questions[i].questiontext] )
    return Response("All good ")
    

#this api is the view responses api. given form id, it returns the related questions, their individual responses
@api_view(['GET'])
@permission_classes([IsAuthenticated])    
def viewresponsesapi(request,pk):
    formidgetforapi = FormMain.objects.filter(id=pk)
    formidget = FormMain.objects.get(id=pk)
    questions = Question.objects.filter(formid = formidget)
    listofanswers =[]
    for i in questions:
        # find all answers related to all questions
        allanswers = Answer.objects.filter(questionid = i)
        for q in allanswers:
            listofanswers.append(q)
    print(listofanswers)
    listofnaswersdata = answerserializer(listofanswers , many= True)
    formdata = FormmainSerializer(formidgetforapi , many = True)
    questionsdata = Questionserializer(questions , many =True) 
    alldata = listofnaswersdata.data + formdata.data + questionsdata.data   
    return Response(alldata)
    
    



# Get all forms : this shows the user, the list of all forms
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def formlist(request):
    forms = FormMain.objects.all()
    serializer = FormmainSerializer(forms , many = True)
    return Response(serializer.data)


# testing login token
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loginonly(request):
    forms = FormMain.objects.all()
    serializer = FormmainSerializer(forms , many = True)
    return Response(serializer.data)

# # Get all questions ///// Pointless after making an endpoint which includes forms
@api_view(['GET'])
def questionlist(request,pk):
    questions = Question.objects.filter(formid = pk)
    serializer = Questionserializer(questions , many = True)
    return Response(serializer.data)



# get question detail
@api_view(['GET'])
def questionlistdetail(request,pk):
    questions = Question.objects.get(id= pk)
    serializer = Questionserializer(questions )
    return Response(serializer.data)

#api testing
@api_view(['GET'])
def apiOverview(request):
    
    return Response("Hello World API is working")


#create form api. This api takes in form data and creates forms, and question and mcq elements if applicable
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def formtakerapi(request):
    serializer = FormmainSerializer(data = request.data)
    print(request.user)
    if serializer.is_valid():
        serializer.save()

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
        print(serializer.errors)
    return Response(serializer.data)





# Views below this are created for templates







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


def formedit(request,pk):
    form = FormMain.objects.get(id=pk)
    questions = Question.objects.filter(formid = pk)
    for que in questions:
        if que.questiontype =="SingleSelect":

            mcqoptions = mcqchoice.objects.filter(questionid = que)
    
    context = {'form':form ,'questions':questions ,'mcqoptions':mcqoptions}
    return render(request,'formedit.html',context)

    
    # return render(request,'formview.html',context)  