from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.views.generic import View
from .models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
# Create your views here.

class TaskList(View):
    def get(self, request):
        form = TaskForm()
        tasks = Task.objects.all()
        return render(request, 'ajax.html', {'form': form, 'tasks': tasks})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save()
            # send task object as json response, this return value is what is in success: function(response)
            return JsonResponse({'task': model_to_dict(new_task)}, status=200)
        else:
            return redirect('task_list_url')



# def post_create(request):
#     data = dict()

#     if request.method == 'POST':
#         form = BlogForm(request.POST)
#         if form.is_valid():
#             form.save()
#             data['form_is_valid'] = True
#         else:
#             data['form_is_valid'] = False
#     return JsonResponse(data)
    