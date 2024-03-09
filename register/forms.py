
from django import forms
from django.forms import ModelForm

from .models import  Attendance, LessonSummary, LessonTopic, OnlineLesson, Person, Student





class PersonForm(ModelForm):

    class Meta:
        model= Person
        fields= '__all__'


class StudentForm(ModelForm):

    class Meta:
        model= Student
        fields= '__all__'
        exclude=['att_count','person','is_enrolled',]




class CommentForm(ModelForm):

    class Meta:
        model= LessonSummary
        fields= '__all__'

    def __init__(self, *args, **kwargs):
        super(CommentForm, self). __init__( *args, **kwargs)
        # var = self.fields['user']
        # var.disabled = True
        
        for key, value in self.fields.items():
            self.fields['lesson'].widget = forms.HiddenInput()
            self.fields['number_of_students'].widget = forms.HiddenInput()








class LessonForm(ModelForm):

    class Meta:

        model= LessonTopic
        fields= '__all__'
        exclude=['is_taught','valid',]


    def __init__(self, *args, **kwargs):
        super(LessonForm, self). __init__( *args, **kwargs)
        var = self.fields['user']
        var.disabled = True
        
        for key, value in self.fields.items():
            self.fields['user'].widget = forms.HiddenInput()
            self.fields['taught_on_date'].help_text =' Date format Year-Month-Day, eg 2024-12-31'


class OnlineLessonForm(ModelForm):

    class Meta:
        model= OnlineLesson
        fields= '__all__'


class AttendaceForm(ModelForm):
    class Meta:
        model=Attendance
        fields= '__all__'
      