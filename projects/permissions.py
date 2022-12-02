# permissions.py
from rest_framework import permissions # permissions import
class IsAuthorOrReadonly(permissions.BasePermission): # BasePermission 상속
    # has_permission
    def has_permission(self, request, view): # 인증된 사용자에 한하여 목록조회/포스트 등록 가능
        return request.user and request.user.is_authenticated
    # has_object_permission
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET, OPTION, HEAD 요청일 때는 그냥 허용
            return True
        return obj.author == request.user # DELETE, PATCH 일 때는 현재 사용자와 객체가 참조 중인 사용자가 일치할 때마다 허용

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 ​​허용되며,
        # 그래서 GET, HEAD, OPTIONS 요청을 허용 할 것입니다.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 인스턴스에는`owner`라는 속성이 있어야합니다.
        return obj.owner == request.user