from django.shortcuts import render
from rest_framework import generics,mixins,status
from .serializers import InstitutionsRegistrSeliarizer, LoginInstutions,FormSerializer,EventSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from Authontication.models import User
from .models import Event,FCreate

# Create your views here.

class InstitutionsAPIView(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=InstitutionsRegistrSeliarizer
    queryset=User.objects.filter(SignUp_as='Institutions')
    def post(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class GetInstitutionAPIView(generics.GenericAPIView,mixins.ListModelMixin):
    # permission_classes=[IsAuthenticated]
    serializer_class=InstitutionsRegistrSeliarizer
    queryset=User.objects.filter(SignUp_as='Institutions')
    def get(self, request):
        return self.list(request)
    
    
class LoginInstutitions(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class=LoginInstutions
    def post (self,request):  
        email=request.data['email']
        password=request.data['password']
        
        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user is not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('password is incorrect')
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
            'iat': datetime.datetime.utcnow()  
        }
        
        token=jwt.encode(payload,'secret', algorithm='HS256')
        response=Response()
        response.set_cookie(key='access', value=token, httponly=True)
        response.data={
                'access':token
            }
        
        return response
    
class FormIPAView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class=FormSerializer
    queryset=FCreate.objects.all()
    lookup_field='id'
    def post(self, request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get (self,request, id=None):
        
        if id:
            return self.retrieve(request)
        else:
            
            return self.list(request)
        
        
class FormDetailsAPIView(generics.GenericAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class=FormSerializer
    queryset=FCreate.objects.all()
    lookup_field='id'
    def put (self,request,id=None):
        return self.update(request, id)
    
    
    def delete(self,request,id=None):
        return self.destroy(request,id)
    
class EventIPAView(generics.GenericAPIView):
    serializer_class=EventSerializer
    queryset=Event.objects.all()
    # lookup_field='id'
    def post(self, request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)