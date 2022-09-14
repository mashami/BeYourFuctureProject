from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['SignUp_as','Disability','first_Name','Last_Name','User_name','create_on','phone_Number']
    list_filter=['SignUp_as','Disability','create_on']