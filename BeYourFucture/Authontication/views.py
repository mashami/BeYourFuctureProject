
# Create your views here.

from django.shortcuts import render
from .serializers import *
from rest_framework import generics, mixins,status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed 
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser 
import jwt,datetime
from django.core.mail import send_mail
from Authontication.serializers import emailserializer
from django.conf import settings
from django.contrib.auth.models import Group,Permission




from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# Create your views here.


class UserIPAView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin):
    serializer_class=UserSiliarizer
    queryset=User.objects.all()
    
    def post(self, request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            SignUp_as = serializer.data['SignUp_as']
            my_group1 = Group.objects.get(name='DisabilityUsersGroup')
            my_group2=Group.objects.get(name='NormalUsersGroup') 
            if SignUp_as=='person without disability':
              my_group1.user_set.add(request.user.id)
            elif SignUp_as=='person with disability':
                my_group2.user_set.add(request.user.id)
            else:
               pass
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        return self.list(request)
    
    def Delete(self,request,id=None):
        return self.destroy(request, id)
    

    
class Login(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class=UserSerializerLogIn
    def post (self,request):  
        User_name=request.data['User_name']
        password=request.data['password']
        
        user=User.objects.filter(User_name=User_name).first()
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
        response.set_cookie(key='Bearer', value=token, httponly=True)
        response.data={
                'Bearer':token
            }
        
        return response



class UserView(APIView):
    # permission_classes=[IsAuthenticated]
    def get(self,request):
        token=request.COOKIES.get('Bearer')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthentacated')
        
        
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSiliarizer(user)
        # othor=serializer.User_name
        return Response(serializer.data)

    
class LogOut(APIView):
    def post(self,request):
        response=Response(status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('jwt')
        
        response.data={
            'message':'user has been logout successful!!' 
        }
        
        return response
    
    
# class sendEmail(APIView):    
#     def post(self, request, format=None):
#         serializer = emailserializer(data=request.data)
#         if serializer.is_valid():
#             send_to = serializer.data['email']
#             content = serializer.data['content']
            
#             email_sender = settings.EMAIL_HOST_USER
#             send_mail(
#                 'Subject here',
#                 content,
#                 email_sender,
#                 [send_to],
#                 fail_silently=False,
#             )
                
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ForgetPassword(APIView):    
    def post(self, request, format=None):
        serializer = emailserializer(data=request.data)
        
        if serializer.is_valid():
            send_to = serializer.data['email']
            email_sender = settings.EMAIL_HOST_USER
            email=request.data['email']
            if User.objects.filter(email=email).exists():
            
                user=User.objects.get(email=email)
                # uidb64=urlsafe_base64_encode(smart_bytes(user.id))
                token=PasswordResetTokenGenerator().make_token(user)
                
                send_mail(
                    'Code verification' 
                    'Use this code To verify',
                    token,
                    email_sender,
                    [send_to],
                    fail_silently=False,
                )
                def __init__(self):
                    self.vri=token
                return Response({'success':True,'message':'send Email successfull to: ','Email':serializer.data},status=status.HTTP_200_OK)
            return Response({'Fail':True,'message':'this Email is not registed in our system'},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# class ResetPassword(generics.GenericAPIView):
    
#     serializer_class=ResetPassordSerializer
#     def post(self,request):
#         serializer=self.serializer_class(data=request.data)
#         email=request.data['email']
        
#         if User.objects.filter(email=email).exists():
            
#             user=User.objects.get(email=email)
#             uidb64=urlsafe_base64_encode(smart_bytes(user.id))
#             token=PasswordResetTokenGenerator().make_token(user)
#             current_site= get_current_site(request=request).domain
#             relativeLink= reverse('passwordReset-confirm',kwargs={'uidb64':uidb64,'token':token})
#             absurl = 'http://'+ current_site+ relativeLink
#             email_body='Hello, \n Use link bellow to Reset your password \n'+absurl
#             data={
#                 'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
#             Util.send_email (data)
#             return Response({'Success':'we have send you  a email for reset password'}, status=status.HTTP_200_OK)
#         return Response({'Not found',status.HTTP_400_BAD_REQUEST})


class verifyToken(generics.GenericAPIView, mixins.CreateModelMixin,ForgetPassword):
    serializer_class=verifyTokenSerializer 
    def __init__(self,Token):
       return self.Token.vri
        
    def post(self,request):
        token=self.serializer_class(data=request.data)
        ClassF=ForgetPassword()
        currentToken=ClassF.self('token')
        print()
        print()
        print()
        print(currentToken)
        print()
        print()
        print()
        serializer=self.serializer_class(data=request.data)
        if token != currentToken:
            raise AuthenticationFailed('token is incorrect')
        serializer.is_valid(raise_exception=True)
        self.create(request)
        return Response({'success':True,'message':'code verified successfull'}, status=status.HTTP_200_OK)
    
    
class SetNewPasswordAPI(generics.GenericAPIView ,mixins.UpdateModelMixin):
    serializer_class=SetNewPasswordserializer
    lookup_field='id'
    def put (self,request, id=None):
        
        return self.update(request,id)

    
class updateUser(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class=UserSiliarizer
    queryset=User.objects.all()
    lookup_field='id'
    # authentication_classes=[SessionAuthentication,BasicAuthentication]
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    def get (self,request, id=None):
        if id:
            return self.retrieve(request)
        else:
            
            return self.list(request)
    
    def put (self,request,id=None):
        return self.update(request, id)
    
    
    def delete(self,request,id=None):
        return self.destroy(request,id)
    
    
# class CreateGroup (generics.GenericAPIView, mixins.CreateModelMixin):
#     serializer_class=CreateGroupSerializer
#     def post(request,self):
#         data=request.data
#         serializer=self.serializer_class(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)