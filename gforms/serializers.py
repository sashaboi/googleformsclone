from rest_framework import serializers
from .models import FormMain , Question ,mcqchoice,Answer
from django.contrib.auth.models import User

class FormmainSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormMain
        fields = '__all__'

class Questionserializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class mcqchoiceserializer(serializers.ModelSerializer):
    class Meta:
        model = mcqchoice
        fields = '__all__'

class answerserializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email' ,'username']

class Allserializer(serializers.Serializer):
    forms = FormmainSerializer(many =True)
    questions = Questionserializer(many =True)
    mcqchoices = mcqchoiceserializer(many =True)
