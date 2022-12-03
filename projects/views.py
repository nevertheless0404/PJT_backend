from django.shortcuts import render
from .models import Project, Todo, Informs, Members, Comment
from accounts.models import User
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from .serializers import (
    ProjectSerializer,
    TodoSerializer,
    InformsSerializer,
    MembersSerializer,
    CommentSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# project의 목록을 보여주는 역할
class Projectlist(APIView):
    permissions_classes = [IsAuthenticated]

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
        if request.user != 0:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():  # 유효성 검사
                serializer.validated_data['user'] = request.user
                serializer.save()  # 저장
                print("==============================================")
                print(serializer.data['id'])
                project = Project.objects.get(pk=serializer.data['id'])
                Members.objects.create(user=request.user, leader=1, project=project)
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
        members = Members.objects.filter(project=project.pk)
        for member in members:
            print('다영사랑해 다영사랑해 다영사랑해')
            if member.user == request.user.email:
                serializer = ProjectSerializer(project)
            return Response(serializer.data)

    # project 수정하기
    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        members = Members.objects.filter(project=project.pk)
        lead = 0
        for member in members:
            print('다영사랑해 다영사랑해 다영사랑해')
            if member.leader == 1:
                lead = member
                if lead.user == request.user.email:
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # project 삭제하기
    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        members = Members.objects.filter(project=project.pk)
        lead = 0
        for member in members:
            if member.leader == 1:
                lead = member
                if lead.user == request.user.email:
                    project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def changeleader(request, project_pk, leader_pk, format=None):
    if request.method == "POST":
        members = Members.objects.get(pk=project_pk)
        nowleader = 0
        for member in members:
            if member.leader == 1:
                nowleader = member
                break
        if request.user == nowleader.user:
            new = User.objects.get(pk=leader_pk)
            newleader = 0
            for member in members:
                if member.user == new.email:
                    member.leader = 1
                    member.save()
                    break
            return Response("변경 성공!", status=status.HTTP_201_CREATED)
        
            # new = User.objects.get(pk=leader_pk)
            # project = Project(user=new)
            # print(project)
            # project.save()
    return Response("변경 실패!", status=status.HTTP_400_BAD_REQUEST)


# todo의 목록을 보여주는 역할
class Todolist(APIView):
    # permissions_classes = [IsAuthenticated]
    # todo list를 보여줄 때
    def get(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        members = Members.objects.filter(project=project)
        print(members)
        for member in members:
            if request.user.email == member.user:
                todos = Todo.objects.filter(project=project)
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
                serializer = TodoSerializer(todos, many=True)
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 todo 글을 작성할 때
    def post(self, request,  project_pk):
        # request.data는 사용자의 입력 데이터
        project = Project.objects.get(pk=project_pk)
        serializer = TodoSerializer(data=request.data)
        members = Members.objects.filter(project=project)
        for member in members:
            if request.user.email == member.user:
                if serializer.is_valid():  # 유효성 검사
                    serializer.validated_data['project'] = project
                    serializer.validated_data['user'] = request.user
                    serializer.save()  # 저장
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# todo의 detail을 보여주는 역할
class Tododetail(APIView):
    permissions_classes = [IsAuthenticated]
    # todo 객체 가져오기
    def get_object(self, project_pk, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

    # todo의 detail 보기
    def get(self, request, project_pk, pk, format=None):
        project = Project.objects.get(pk=project_pk)
        serializer = TodoSerializer(data=request.data)
        members = Members.objects.filter(project=project)
        for member in members:
            if request.user.email == member.user:
                todo = self.get_object(pk)
                serializer = TodoSerializer(todo)
                return Response(serializer.data)

    # todo 수정하기
    def put(self, request, project_pk,  pk, format=None):
        project = Project.objects.get(pk=project_pk)
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo, data=request.data)
        if todo.user == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # todo 삭제하기
    def delete(self, request, project_pk, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Ptoj(APIView):
    def get(self, request):
        mytodo = Todo.objects.filter(user=request.user)
        serializer1 = TodoSerializer(mytodo, many=True)
        return Response(serializer1.data)

# 공지사랑 리스트 생성
class Informslist(APIView):
    def get(self, request, pk):
        inform = Informs.objects.filter(project=pk)
        serializer = InformsSerializer(inform, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        teamleader = 0
        leaders = Members.objects.filter(project=pk)
        for lead in leaders:
            if lead.leader == 1:
                teamleader = lead
                break
        if request.user.email == lead.user:
            serializer = InformsSerializer(data=request.data)
            project = Project.objects.get(pk=pk)
            if serializer.is_valid():
                serializer.validated_data['project'] = project
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
        members = Members.objects.filter(project_id=pk)
        serializer = MembersSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        project = Project.objects.get(pk=pk)
        print(request.data)
        for dt in request.data:
            print(dt)
            serializer = MembersSerializer(data=dt)
            if serializer.is_valid():
                serializer.validated_data['project'] = project
                # print(serializer.validated_data)
                serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def comment(request,  project_pk, todo_pk):
    serializer = CommentSerializer(data=request.data)
    comments = Comment.objects.filter(todo_id=todo_pk)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def comment_create(request, project_pk, todo_pk):
    serializer = CommentSerializer(data=request.data)
    todo = get_object_or_404(Todo, pk=todo_pk)
    if serializer.is_valid(raise_exception=True):
        serializer.save(todo=todo)
        return Response(serializer.data)

@api_view(['PUT','DELETE'])
def comment_update_and_delete(request, project_pk, todo_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Comment has been updated!'})
    else:
        comment.delete()
    return Response({'message':'Comment has been deleted!'})
