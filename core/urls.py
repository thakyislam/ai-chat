from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('prompt/<int:prompt_id>/', views.prompt_detail, name='prompt_detail'),
]