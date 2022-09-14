
from django.db import models
from Authontication.models import User
# Create your models here.
 
    
class FCreate(models.Model):
    Nation_Id=models.PositiveIntegerField(max_length=16)
    your_Names=models.CharField(max_length=100,null=False,blank=False)
    NamesHelp=models.ForeignKey(User,on_delete=models.CASCADE, related_name='UsernameForm')
    phone_number=models.CharField(max_length=50)
    Description=models.TextField(max_length=254)
    created_on=models.DateField(auto_now_add=True)
    
    def __str__(self) :
        return self.your_Names
    
class partnershipsInsitutions(models.Model):
   
    UserName=models.ForeignKey(FCreate, max_length=100, on_delete=models.CASCADE, related_name='User_Name') 
    
   
    def __str__(self):
        return self.UserName
    
  
    
class Event (models.Model):
    
    # InstitutionName = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Institution_Name')
    InstitutionName = models.CharField(max_length=100)
    title = models.TextField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images/",blank=True, null=True)
    video=models.FileField(upload_to='post_video', null=True, blank=True)
    Discription=models.TextField(max_length=255, blank=True, null=True)
    # slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

    