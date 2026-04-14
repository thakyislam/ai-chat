from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dress-suggestion/', views.dress_suggestion, name='dress_suggestion'),
]