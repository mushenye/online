

from django.forms import ModelForm

from .models import  LessonTopic, Person, Student


class PersonForm(ModelForm):

    class Meta:
        model= Person
        fields= '__all__'


class StudentForm(ModelForm):

    class Meta:
        model= Student
        fields= '__all__'


class LessonForm(ModelForm):

    class Meta:
        model= LessonTopic
        fields= '__all__'