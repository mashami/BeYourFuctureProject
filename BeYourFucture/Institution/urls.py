from django.urls import path
from . import views
urlpatterns = [
    path('/registration/',views.InstitutionsAPIView.as_view()),
    path('/get/',views.GetInstitutionAPIView.as_view()),
    path('/login_institution', views.LoginInstutitions.as_view()),
    
    path('/createForm/', views.FormIPAView.as_view()),
    path('/formDetail/',views.FormDetailsAPIView.as_view()),
    path('/event/',views.EventIPAView.as_view()),
    
    
]