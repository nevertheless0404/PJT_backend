from django.db import models
from django.conf import settings

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=30)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name= 'project_user')
    goal = models.CharField(max_length=50)
    skill = models.TextField()
    functions = models.TextField()
    leader = models.CharField(max_length=20)
    members = models.TextField()

class Todo(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name= 'todo_user')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name= 'todo_project')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()