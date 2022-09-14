from django.contrib import admin
from .models import *
from Authontication.models import User
# Register your models here.
# admin.site.register(User.objects.get(SignUp_as='Institutions'))
admin.site.register(partnershipsInsitutions)
admin.site.register(FCreate)
admin.site.register(Event)



    