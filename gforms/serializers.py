from rest_framework import serializers
from .models import FormMain , Question ,mcqchoice

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