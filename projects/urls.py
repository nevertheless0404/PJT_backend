from django.urls import path, include

# from .views import ProjectViewSet, TodoViewSet
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# # 첫 번째 인자는 url의 prefix
# # 두 번째 인자는 ViewSet
# router.register('project', ProjectViewSet)
# router.register('Todo', TodoViewSet)

# urlpatterns =[
#     path('', include(router.urls)),
# ]

from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("project/", views.Projectlist.as_view()),
    path("project/<int:pk>/", views.Projectdetail.as_view()),
    path("recent_project/", views.RecentProjectlist.as_view()),
    path("<int:project_pk>/todo/", views.Todolist.as_view()),
    path("<int:project_pk>/todo/<int:todo_pk>/", views.Tododetail.as_view()),
    path("<int:project_pk>/todo/<int:todo_pk>/comment/", views.Commentlist.as_view()),
    path("<int:project_pk>/todo/<int:todo_pk>/comment/<int:comment_pk>/",views.Commentdetail.as_view()),
    path("ptoj/", views.Ptoj.as_view()),
    path("informs/<int:pk>/", views.Informslist.as_view()),
    path("informs/<int:pk>/", views.Informsdetail.as_view()),
    path("memberadmin/<int:pk>/", views.Membersadm.as_view()),
    path("memberadmin/<int:project_pk>/<int:pk>/", views.Membersadmdetail.as_view()),
    path("changeleader/<int:project_pk>/<int:leader_pk>/", views.changeleader),
    path("<int:pk>/markdown/", views.Markdowndetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
#
