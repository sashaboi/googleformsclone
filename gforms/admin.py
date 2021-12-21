from django.contrib import admin
from gforms.models import FormMain , Question, Answer, mcqchoice

admin.site.register(FormMain)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(mcqchoice)

# Register your models here.
