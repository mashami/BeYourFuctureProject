from urllib import request
from django.shortcuts import render
from rest_framework import generics, mixins, status
from .serializer import PostSerializer
from .models import Post
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.contrib import auth
from .permissions import PostPermission,DisabilityUserPermission
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.
class PostAPIView(generics.GenericAPIView,mixins.ListModelMixin):
    permission_classes=[IsAuthenticated,DisabilityUserPermission]
    serializer_class=PostSerializer
    # username=request.data
    # gta = Post.objects.create(name="gta", auth=?)
    
    # user=auth.authenticate(username=username)
    queryset=Post.objects.all()
    def post(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            print('')
            print('')
            print('')
            print('')
            print('')
            print('')
            print('')
            print('')
            print("User is logged in :)")
            print(f"Username --> {request.user.username}")
            print('')
            print('')
            print('')
            print('')
            print('')
            print('')
            user=request.user.username
            author=PostSerializer().author
            user=author
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED )
   
            # else:
            #     Post.author=None
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get (self,request):
        permission_classes=[IsAuthenticated]
        return self.list(request)
    
    
class PostAPIADetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated,PostPermission,DisabilityUserPermission]
    # lookup_field='id'
    serializer_class=PostSerializer
    queryset=Post.objects.all()
    # def put(self, request,id=None):
        
    #     return self.update(request,id)
    
    # def delete(self,request,id=None):
    #     return self.destroy(request,id)
