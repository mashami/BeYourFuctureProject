
from rest_framework import serializers
from .models import Post
class PostSerializer(serializers.ModelSerializer):
    auth=serializers.CharField(read_only=True)
    class Meta:
        model=Post
        fields=['image','video','title','content','auth']
    
    def get_author(self,request):
        self.auth=request.user.username
        return self.auth