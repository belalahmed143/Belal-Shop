from django.db import models
from ckeditor.fields import RichTextField
from django_quill.fields import QuillField
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    dis = RichTextField(default=2)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering= ['-id']