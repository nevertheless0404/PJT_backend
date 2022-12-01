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
    path("todo/", views.Todolist.as_view()),
    path("todo/<int:pk>/", views.Tododetail.as_view()),
    path("ptoj/", views.Ptoj.as_view()),
    path("informs/", views.Informslist.as_view()),
    path("informs/<int:pk>/", views.Informsdetail.as_view()),
    path("memberadmin/<int:pk>/", views.Membersadm.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
