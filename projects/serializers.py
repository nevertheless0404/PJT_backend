from .models import Project, Todo, Informs, Members, Comment, Markdown
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
        fields = ["id","title","start_at","end_at","content","complete","comments"]

class MarkdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markdown
        fields = ["project", "content"]

class ProjectSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ["id","title","start_at", "end_at","goal","skill","functions", "user_id"]

class RecentProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id"]

class InformsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informs
        fields = ['content']

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id','user']