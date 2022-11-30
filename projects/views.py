from django.shortcuts import render
from .models import Project, Todo
from .serializers import ProjectSerializer, TodoSerializer
from rest_framework import viewsets

# Create your views here.
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

# class TodoViewSet(viewsets.ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer


# 데이터 처리
from .models import Project, Todo
from .serializers import ProjectSerializer, TodoSerializer

# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# project의 목록을 보여주는 역할
class Projectlist(APIView):
    # project list를 보여줄 때
    def get(self, request):
        projects = Project.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    # 새로운 project 글을 작성할 때
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# project의 detail을 보여주는 역할
class Projectdetail(APIView):
    # project 객체 가져오기
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    # project의 detail 보기
    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    # project 수정하기
    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # project 삭제하기
    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








# todo의 목록을 보여주는 역할
class Todolist(APIView):
    # todo list를 보여줄 때
    def get(self, request):
        todos = Todo.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    # 새로운 todo 글을 작성할 때
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# todo의 detail을 보여주는 역할
class Tododetail(APIView):
    # todo 객체 가져오기
    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404
    
    # todo의 detail 보기
    def get(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    # todo 수정하기
    def put(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # todo 삭제하기
    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)