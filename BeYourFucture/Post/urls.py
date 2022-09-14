from django.urls import path
from . import views
urlpatterns = [
    path('post/',views.PostAPIView.as_view()),
    path('post-detail/<int:id>/', views.PostAPIADetails.as_view()),
]