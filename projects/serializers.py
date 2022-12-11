from .models import Project, Todo, Informs, Members, Comment, Markdown, Notification
from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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
        fields = ["id","title","start_at","end_at","content", "complete", "comments"]

class MarkdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markdown
        fields = ["project", "content"]

class ProjectSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ["id","title","start_at","end_at","goal","skill","functions", "todo_project", "comments", "color"]


class RecentProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id"]

class InformsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informs
        fields = ['id', 'content']

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    send_user = UserSerializer(read_only=True)
    receive_user = UserSerializer(read_only=True)
    is_read = serializers.ReadOnlyField()
    todo = TodoSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'