from django.urls import path 
from . import views 
urlpatterns = [ 
    path('', views.index), 
    path('/login', views.user_login),
    path('/reg', views.user_reg),
    path('/logout', views.user_logout) 
] 
