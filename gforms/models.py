from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
# Create your models here.
class FormMain(models.Model):
    formname = models.CharField(max_length=200)
    csvfile =models.FileField(upload_to='csvs',blank=True)
    usethisbool = models.BooleanField(default=False )
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    ,default=1)
    def __str__(self):
            return self.formname


class Question(models.Model):
    
    formid = models.ForeignKey(FormMain,on_delete=models.CASCADE)
    questiontext = models.CharField(max_length=200)
    questiontype = models.CharField(max_length=200)
    questionnumber = models.IntegerField()
    required =models.BooleanField()

    def __str__(self):
            return self.questiontext

class Answer(models.Model):
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    ,default=1)
    questionid = models.ForeignKey(Question,on_delete=CASCADE)
    answerdata = models.CharField(max_length=200)

    def __str__(self):
            return self.questionid.questiontext

class mcqchoice (models.Model):
    questionid = models.ForeignKey(Question,on_delete=CASCADE)
    choice = models.CharField(max_length=200, blank=True)
    
    
    def __str__(self):
            return self.choice
