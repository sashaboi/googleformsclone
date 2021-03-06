# Generated by Django 4.0 on 2021-12-20 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formname', models.CharField(max_length=200)),
                ('userid', models.CharField(max_length=200)),
                ('createdat', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=200)),
                ('questiontext', models.CharField(max_length=200)),
                ('questiontype', models.CharField(max_length=200)),
                ('questionnumber', models.IntegerField()),
                ('required', models.BooleanField()),
                ('formid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gforms.formmain')),
            ],
        ),
        migrations.CreateModel(
            name='mcqchoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(blank=True, max_length=200)),
                ('questionid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gforms.question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=200)),
                ('answerdata', models.CharField(max_length=200)),
                ('questionid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gforms.question')),
            ],
        ),
    ]
