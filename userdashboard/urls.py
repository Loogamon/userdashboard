from django.contrib import admin 
from django.urls import path, include 
urlpatterns = [ 
    path('', include('app.urls'))
] 
#handler404 = "app.views.what"