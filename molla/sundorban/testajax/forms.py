from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
class TaskForm(forms.ModelForm):
    class Meta:   
        model = Task
        fields = ['title','dis']

        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }