from .models import Project, Todo, Informs, Members, Comment
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class InformsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informs
        fields = '__all__'

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['user','project']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment',]