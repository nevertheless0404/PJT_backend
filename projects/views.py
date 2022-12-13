from django.shortcuts import render
from .models import Project, Todo, Informs, Members, Comment, Markdown, Notification
from accounts.models import User
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
import random
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class RecentProjectlist(APIView):
    def get(self, request):
        project = Project.objects.filter(user_id=request.user.pk).order_by("-pk")[0]
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


# project의 목록을 보여주는 역할
class Projectlist(APIView):
    permissions_classes = [IsAuthenticated]

    # project list를 보여줄 때``
    def get(self, request):
        members = Members.objects.filter(user=request.user)
        projects = []
        for member in members:
            # 참여하는 프로젝트 보여짐
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
                # 유저 추가해주기
                serializer.validated_data["user"] = request.user
                x = random.randrange(1, 4)
                serializer.validated_data["color"] = x
                serializer.save()  # 저장
                project = Project.objects.get(pk=serializer.data["id"])
                # 멤버스 안에 만든사람 db에 저장하기
                Members.objects.create(user=request.user, leader=1, project=project)
                members = Members.objects.filter(project_id=serializer.data["id"])
                members_list = ""
                skills_list = ""
                functions_list = ""
                for member in members:
                    members_list += "- " + member.user + "\n"
                for skill in project.skill.split(" "):
                    skills_list += "- " + skill + "\n"
                for function in project.functions.split(" "):
                    functions_list += "- " + function + "\n"
                # Markdown 안에 프로젝트 내용 저장하기
                content = (
                    "# "
                    + project.title
                    + "\n"
                    + "## 서비스 목표 "
                    + "\n"
                    + project.goal
                    + "\n"
                    + "## 개발 기간 "
                    + "\n"
                    + str(project.start_at)
                    + " ~ "
                    + str(project.end_at)
                    + "\n"
                    + "## 팀원 "
                    + "\n"
                    + members_list
                    + "\n"
                    + "## 기술 스택 "
                    + "\n"
                    + skills_list
                    + "\n"
                    + "## 주요 기능 "
                    + "\n"
                    + functions_list
                )
                Markdown.objects.create(project=project, content=content)
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
        # 멤버스에 있는 사람만 디테일 볼 수 있음
        members = Members.objects.filter(project=project.pk)
        for member in members:
            if member.user == request.user.email:
                serializer = ProjectSerializer(project)
                return Response(serializer.data)

    # project 수정하기
    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        # 팀장인 사람만 project수정 가능
        members = Members.objects.filter(project=project.pk)
        markdown = Markdown.objects.get(project_id=pk)
        lead = 0
        for member in members:
            if member.leader == 1:
                lead = member
                if lead.user == request.user.email:
                    if serializer.is_valid():
                        serializer.save()
                        members_list = ""
                        skills_list = ""
                        functions_list = ""
                        for member in members:
                            members_list += "- " + member.user + "\n"
                        for skill in project.skill.split(" "):
                            skills_list += "- " + skill + "\n"
                        for function in project.functions.split(" "):
                            functions_list += "- " + function + "\n"
                        content = (
                            "# "
                            + project.title
                            + "\n"
                            + "## 서비스 목표 "
                            + "\n"
                            + project.goal
                            + "\n"
                            + "## 개발 기간 "
                            + "\n"
                            + str(project.start_at)
                            + " ~ "
                            + str(project.end_at)
                            + "\n"
                            + "## 팀원 "
                            + "\n"
                            + members_list
                            + "\n"
                            + "## 기술 스택 "
                            + "\n"
                            + skills_list
                            + "\n"
                            + "## 주요 기능 "
                            + "\n"
                            + functions_list
                        )
                        markdown.content = content
                        markdown.save()
                        return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # project 삭제하기
    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        # 팀장만 project 삭제 가능
        members = Members.objects.filter(project=project.pk)
        lead = 0
        for member in members:
            if member.leader == 1:
                lead = member
                if lead.user == request.user.email:
                    project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# markdown detail을 보여주는 역할
class Markdowndetail(APIView):
    def get(self, request, pk):
        markdown = Markdown.objects.get(project_id=pk)
        serializer = MarkdownSerializer(markdown)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        markdown = Markdown.objects.get(project_id=pk)
        serializer = MarkdownSerializer(markdown, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 리더 권한 넘겨주기
@api_view(["GET", "POST"])
def changeleader(request, project_pk, leader_pk, format=None):
    if request.method == "GET":
        # 프로젝트 가져옴
        members = Members.objects.filter(project=project_pk)
        # 현재 리더 변수 할당
        nowleader = 0
        # 멤버 돌리면서 현재 리더 찾기
        for member in members:
            if member.leader == 1:
                nowleader = member
                break
        member = Members.objects.get(pk=leader_pk)
        user = User.objects.get(email=member.user)
        # 현재 리더와 로그인한 유저가 같으면
        if request.user.email == nowleader.user:
            # 유저정보를 가져온다
            newleader_tmp = User.objects.get(pk=user.pk)
            for member in members:
                if member.user == newleader_tmp.email:
                    newleader = member
            newleader.leader = 1
            newleader.save()
            nowleader.leader = 0
            nowleader.save()
        return Response("변경 성공!", status=status.HTTP_201_CREATED)
    return Response("변경 실패!", status=status.HTTP_400_BAD_REQUEST)


# todo의 목록을 보여주는 역할
class Todolist(APIView):
    # permissions_classes = [IsAuthenticated]
    # todo list를 보여줄 때
    def get(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        # 프젝에 있는 유저면 볼 수 있음
        members = Members.objects.filter(project=project)
        for member in members:
            if request.user.email == member.user:
                # 그 프젝의 할 일만 나옴
                todos = Todo.objects.filter(project_id=project_pk)
                serializer = TodoSerializer(todos, many=True)
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 todo 글을 작성할 때
    def post(self, request, project_pk):
        print("todotodotodotodto", request, request.user)
        project = Project.objects.get(pk=project_pk)
        serializer = TodoSerializer(data=request.data)
        # 프젝에 있는 멤버
        members = Members.objects.filter(project=project)
        for member in members:
            if request.user.email == member.user:
                if serializer.is_valid():  # 유효성 검사
                    # 할일에 프젝정보랑 유저정보 넣어줌
                    serializer.validated_data["project"] = project
                    serializer.validated_data["user"] = request.user
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Tododetail(APIView):
    permissions_classes = [IsAuthenticated]
    # todo 객체 가져오기
    def get_object(self, project_pk, todo_pk):
        print(project_pk, todo_pk)
        try:
            return Todo.objects.get(project_id=project_pk, pk=todo_pk)
        except Todo.DoesNotExist:
            raise Http404

    # todo의 detail 보기
    def get(self, request, project_pk, todo_pk, format=None):
        todo = self.get_object(project_pk, todo_pk)
        serializer = TodoSerializer(data=request.data)
        # 프로젝트안의 멤버만 투두 보기
        members = Members.objects.filter(project=project_pk)
        for member in members:
            if request.user.email == member.user:
                serializer = TodoSerializer(todo)
                return Response(serializer.data)

    # todo 수정하기
    def put(self, request, project_pk, todo_pk, format=None):
        todo = self.get_object(project_pk, todo_pk)
        serializer = TodoSerializer(todo, data=request.data)
        if todo.user == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # todo 삭제하기
    def delete(self, request, project_pk, todo_pk, format=None):
        todo = self.get_object(project_pk, todo_pk)
        if todo.user == request.user:
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
                serializer.validated_data["project"] = project
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
        inform = Informs.objects.get(project_id=pk)
        serializer = InformsSerializer(inform)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        inform = Informs.objects.get(project_id=pk)
        serializer = InformsSerializer(inform, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        inform = Informs.objects.get(project_id=pk)
        inform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 멤버 추가
class Membersadm(APIView):
    def get(self, request, pk):
        members = Members.objects.filter(project_id=pk)
        serializer = MembersSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        print(request.user)
        teamleader = 0
        leaders = Members.objects.filter(project=pk)
        for lead in leaders:
            if lead.leader == 1:
                teamleader = lead
                print(lead)
                break
        if request.user.email == lead.user:
            serializer = MembersSerializer(data=request.data)
            project = Project.objects.get(pk=pk)
            if serializer.is_valid():
                serializer.validated_data["project"] = project
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Membersadmdetail(APIView):
    def get_object(self, project_pk, pk):
        try:
            return Members.objects.get(pk=pk)
        except Members.DoesNotExist:
            raise Http404

    def delete(self, request, project_pk, pk, format=None):
        member = self.get_object(project_pk, pk)
        project = Project.objects.get(pk=project_pk)
        members = Members.objects.filter(project=project)
        dele = False
        for i in members:
            if str(i.user) == str(request.user):
                if i.leader == 1:
                    dele = True
        if str(member.user) == str(request.user):
            dele = True
        if dele == True:
            if member.leader == 0:
                member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# comment의 목록을 보여주는 역할
class Commentlist(APIView):
    permissions_classes = [IsAuthenticated]

    # comment list를 보여줄 때``
    def get(self, request, project_pk, todo_pk):
        comments = Comment.objects.filter(project_id=project_pk, todo_id=todo_pk)
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # 새로운 comment를 작성할 때
    def post(self, request, project_pk, todo_pk):
        # request.data는 사용자의 입력 데이터
        serializer = CommentSerializer(data=request.data)
        # todo = get_object_or_404(Todo, pk=todo_pk, project_id=project_pk)
        project = Project.objects.get(pk=project_pk)
        todo = Todo.objects.get(pk=todo_pk)
        if serializer.is_valid():  # 유효성 검사
            serializer.validated_data["user"] = request.user
            serializer.validated_data["project"] = project
            serializer.validated_data["todo"] = todo
            serializer.save()  # 저장
            Notification.objects.create(
                send_user=request.user,
                receive_user=todo.user,
                todo=todo,
                project=project,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# comemnt의 detail을 보여주는 역할
class Commentdetail(APIView):
    # comment 객체 가져오기
    def get_object(self, request, project_pk, todo_pk, comment_pk):
        try:
            return Comment.objects.get(
                project_id=project_pk, todo_id=todo_pk, pk=comment_pk
            )
        except Project.DoesNotExist:
            raise Http404

    # comment의 detail 보기
    def get(self, request, project_pk, todo_pk, comment_pk, format=None):
        print(project_pk, todo_pk, comment_pk)
        comment = Comment.objects.get(
            project_id=project_pk, todo_id=todo_pk, pk=comment_pk
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # 새로운 recomment를 작성할 때
    def post(self, request, project_pk, todo_pk, comment_pk):
        # request.data는 사용자의 입력 데이터
        serializer = CommentSerializer(data=request.data)
        # todo = get_object_or_404(Todo, pk=todo_pk, project_id=project_pk)
        project = Project.objects.get(pk=project_pk)
        todo = Todo.objects.get(pk=todo_pk)
        comment = Comment.objects.get(pk=comment_pk)
        if serializer.is_valid():  # 유효성 검사
            serializer.validated_data["user"] = request.user
            serializer.validated_data["parent"] = comment
            serializer.validated_data["project"] = project
            serializer.validated_data["todo"] = todo
            serializer.save()  # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # comment 수정하기
    def put(self, request, project_pk, todo_pk, comment_pk, format=None):
        comment = Comment.objects.get(
            project_id=project_pk, todo_id=todo_pk, pk=comment_pk
        )
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # comment 삭제하기 #
    def delete(self, request, project_pk, todo_pk, comment_pk, format=None):
        comment = Comment.objects.get(
            project_id=project_pk, todo_id=todo_pk, pk=comment_pk
        )
        if comment.user == request.user:
            comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationList(APIView):
    def get(self, request):
        notifications = Notification.objects.filter(
            receive_user_id=request.user.pk, is_read=0
        )

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class Isread(APIView):
    def put(self, request, pk, format=None):
        notification = Notification.objects.get(pk=pk)
        notification.is_read = 1
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Userlist(APIView):
    def get(self, request, word):

        users = User.objects.filter(email__contains=word)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
