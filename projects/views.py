from django.shortcuts import render
from .models import Project, Todo, Informs,  Members
from accounts.models import User
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .serializers import ProjectSerializer, TodoSerializer, InformsSerializer, MembersSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404

# project의 목록을 보여주는 역할
class Projectlist(APIView):
    # project list를 보여줄 때``
    def get(self, request):
        print(request.user)
        members = Members.objects.filter(user=request.user)
        projects = []
        for member in members:
            print(member.project.pk)
            project = Project.objects.get(pk=member.project.pk)
            projects.append(project)
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    # 새로운 project 글을 작성할 때
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():  # 유효성 검사
            serializer.save()  # 저장
            print(type(serializer.data['id']))
            project = Project.objects.get(pk=serializer.data['id'])
            Members.objects.create(user=request.user, leader=1, project=project )
            
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
        if serializer.is_valid():  # 유효성 검사
            serializer.save()  # 저장
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


class Ptoj(APIView):
    def get(self, request):
        mytodo = Todo.objects.filter(user=request.user)
        serializer1 = TodoSerializer(mytodo, many=True)
        return Response(serializer1.data)


# todo의 목록을 보여주는 역할

class Todolist(APIView):
    # todo list를 보여줄 때
    def get(self, request):
        todos = Todo.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

# 공지사랑 리스트 생성
class Informslist(APIView):
    def get(self, request):
        inform = Informs.objects.all()
        serializer = InformsSerializer(inform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InformsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 공지사항 디테일

class Informsdetail(APIView):
    def get_object(self, pk):
        try:
            return Informs.objects.get(pk=pk)
        except Informs.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        inform = self.get_object(pk)
        serializer = InformsSerializer(inform)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        inform = self.get_object(pk)
        serializer = InformsSerializer(inform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        inform = self.get_object(pk)
        inform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Membersadm(APIView):
    
    def get(self, request, pk):
        members = Members.objects.filter(project_id = pk)
        serializer = MembersSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = MembersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
