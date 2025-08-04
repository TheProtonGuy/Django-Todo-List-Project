from . import views
from django.urls import path

urlpatterns = [
   path('test-home/', views.home, name='test-home'),
   path('register/', views.register, name='register'),
   path('login/', views.login_user, name='login'),
   path('logout/', views.logout_user, name='logout'),
]