
from urllib import request
from xml.dom import ValidationErr
from .models import User
from rest_framework import serializers
from rest_framework.response import Response
from phonenumber_field.modelfields import PhoneNumberField


from multiprocessing import AuthenticationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse




#     new_group, created = Group.objects.get_or_create(name='DisabilityUsersGroup')
#     new_group, created= Group.objects.get_or_create(name='NormalUsersGroup')


class UserSiliarizer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True,write_only=True)
    email=serializers.EmailField()
    class Meta:
        model=User
        fields=['SignUp_as','first_Name','Last_Name','User_name','email','create_on','Disability','phone_Number','is_active','password','confirm_password']
  
        extra_kwargs = {
            'password': {'write_only':True},
            'confirm_password':{'write_only':True},
            'is_active':{'read_only':True},
         }
    
    # def validate(self, data):
    #     email = data.get('email', None)
    #     if email:
    #         data['Username'] = email
    #     return data
        
    def validate_email(self,email):
        existing_email=User.objects.filter(email=email).first()
        if existing_email:
            raise serializers.ValidationError("this Email is already exist!!")
        return email
    
    
    
    def validate(self, attrs):
        phoneNumber_exits=User.objects.filter(User_name=attrs['phone_Number']).exists()
        if phoneNumber_exits:
            raise ValidationErr(details="phone_Number name is already exists")
        
        password= attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if password !=confirm_password:
            raise serializers.ValidationError(
                "password and confirm_password does not match"
            )
        SignUp_as=attrs.get('SignUp_as')
        
        # Disability=attrs.get('Disability')
        if SignUp_as == 'person without disability':
            Disability=None
        
        return attrs
    def create(self, validated_data):
        password= validated_data.pop('password',None)
        confirm_password= validated_data.pop('confirm_password',None)
        instance=User.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)  
            instance.save()
        return instance
# ====================================================================================================

    
    
    # =============================================================================================================
class UserSerializerLogIn(serializers.ModelSerializer):
     class Meta:
        model=User
        fields=['id','User_name','password']
        extra_kwargs = {
            'password': {'write_only':True},
         }
        
class emailserializer(serializers.Serializer):
    email = serializers.EmailField()
    
class SetNewPasswordserializer(serializers.Serializer):
    password=serializers.CharField(min_length=3,max_length=100, write_only=True)
    confirm_password=serializers.CharField(min_length=3,max_length=100, write_only=True)
    
    class Meta:
        fields=['password','confirm_password']
        extra_kwargs = {
            'password': {'write_only':True},
            'confirm_password':{'write_only'}
         }
    
    
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')
            
            if password !=confirm_password:
                raise serializers.ValidationError(
                    "password and confirm_password does not match"
                )
            # id=force_str(urlsafe_base64_decode(uidb64))
            
            if not PasswordResetTokenGenerator().check_token():
                raise AuthenticationError('This link is already used',401)
            
            return attrs
        
        except Exception as e:
            raise AuthenticationError('This link is already used',401)
       
    def update(self, validated_data):
        password= validated_data.pop('password',None)
        confirm_password= validated_data.pop('confirm_password',None)
        instance=User.objects.update.__get__(id=id)(**validated_data)
        if password is not None:
            instance.set_password(password)  
            instance.save()
        return instance
    
    
    
    
class verifyTokenSerializer(serializers.Serializer):
    
    token=serializers.CharField(min_length=1, write_only=True)
    
        
    def validate(self, attrs):
        try:
            token=attrs.get('token')
            if not PasswordResetTokenGenerator().check_token():
                raise AuthenticationError('This verification code is already used',401)
            
            return attrs
        
        except Exception as e:
            raise AuthenticationError('This verification code is already used',401)