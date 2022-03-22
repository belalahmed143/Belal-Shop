from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('tasks/', TaskList.as_view(), name = 'task_list_url')
]