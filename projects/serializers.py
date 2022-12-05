from .models import Project, Todo, Informs, Members, Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    todo = serializers.ReadOnlyField(source="todo.pk")
    class Meta:
        model = Comment
        fields = '__all__'

class TodoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Todo
        fields = ["id","title","start_at","end_at","content", "comments"]

class ProjectSerializer(serializers.ModelSerializer):
    todo_project = TodoSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Project
        fields = ["id","title","start_at","end_at","goal","skill","functions", "todo_project", "comments"]

class InformsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informs
        fields = ['content']

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id','user']