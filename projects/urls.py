from django.urls import path, include
from .views import ProjectViewSet, TodoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
router.register('project', ProjectViewSet)
router.register('Todo', TodoViewSet)

urlpatterns =[
    path('', include(router.urls)),
]