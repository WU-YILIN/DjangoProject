from django.contrib import admin
from django.urls import path, include  # 确保正确导入 path

from main import views
from main.views import index, register, add_phone, add_review
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add_phone/', add_phone, name='add_phone'),
    path('add_review/', add_review, name='add_review'),
    path('reviews/<str:model_name>/', views.model_reviews, name='model_reviews'),
    path('profile/', views.profile, name='profile')

]