from rest_framework.permissions import SAFE_METHODS, BasePermission,BasePermissionMetaclass
from .models import Post
# from Authontication.models import User
from django.contrib.auth import get_user_model
#  SAFE_METHODS, which is a tuple containing 'GET', 'OPTIONS' and 'HEAD'.

User=get_user_model()
class PostPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
        # return super().has_object_permission(request, view, obj)

class DisabilityUserPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        DisabilityUser=User.objects.filter(User.SignUp_as=="person with disability")
        if request.user==DisabilityUser:
            return True
        raise ArithmeticError(
            'To post is only for those people with disability'
        )
        # return super().has_permission(request, view)