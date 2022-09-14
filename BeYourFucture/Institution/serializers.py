from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from Authontication.models import User
from .models import Event,FCreate




class InstitutionsRegistrSeliarizer(serializers.ModelSerializer):
    SignUp_as=serializers.ReadOnlyField(default='Institution')  
    confirm_password=serializers.CharField(required=True,write_only=True)
    email=serializers.EmailField()
    # SignUp_as='Institutions'
    class Meta:
        model=User
        fields=['SignUp_as','User_name','email','create_on','is_active','password','confirm_password']
        
        extra_kwargs = {
            'password': {'write_only':True},
            'confirm_password':{'write_only':True},
            'is_active':{'read_only':True},
         }
    
    
    def validate_email(self,email):
        existing_email=User.objects.filter(email=email).first()
        if existing_email:
            raise serializers.ValidationError("this Email is already exist!!")
        return email
    
    
    
    def validate(self, attrs):
        password= attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if password !=confirm_password:
            raise serializers.ValidationError(
                "password and confirm_password does not match"
            )
        # SignUp_as=attrs.get('SignUp_as')
        # if SignUp_as !='Institutions':
        #     raise  serializers.ValidationError(
        #         "This is Registrations is for The institutions only "
        #     )
        return attrs
    
    
    def create(self, validated_data):
        password= validated_data.pop('password',None)
        confirm_password= validated_data.pop('confirm_password',None)
        instance=User.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.SignUp_as == 'Institutions'
            instance.save()
        return instance


        
        
class LoginInstutions(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['email','password']
        
        extra_kwargs = {
            'password': {'write_only':True},
         }
        
class FormSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=FCreate
        fields='__all__'
        
class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Event
        fields='__all__'
        