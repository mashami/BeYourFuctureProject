from django.urls import path
from . import views

urlpatterns = [

    path('signUp',views.UserIPAView.as_view()),
    path('login/',views.Login.as_view()),
    path('userlogedin/',views.UserView.as_view()),
    path('logout/',views.LogOut.as_view()),
    path('forgetpassword/',views.ForgetPassword.as_view()),
    path('resetpassowrd',views.SetNewPasswordAPI.as_view()),
    path('verify/',views.verifyToken.as_view()),
    path('update/<int:id>',views.updateUser.as_view()),
]