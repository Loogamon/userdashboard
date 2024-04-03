from django.urls import path 
from . import views, posts 
urlpatterns = [ 
    path('', views.index),
    #path('debug', views.debug),
    path('post/admins/add', posts.admins_add),
    path('post/admins/edit/info', posts.admins_edit_info),
    path('post/admins/edit/password', posts.admins_edit_password),
    path('post/users/edit/info', posts.users_edit_info),
    path('post/users/edit/password', posts.users_edit_password),
    path('post/users/edit/desc', posts.users_edit_desc),
    path('post/msgs/profile', posts.msgs_profile),
    path('post/msgs/message', posts.msgs_message),
    path('users/delete/<int:id>', posts.delete_user),
    path('comments/delete/<int:id>', posts.delete_comment),
    path('subcomments/delete/<int:id>', posts.delete_subcomment),
    
    path('users/reg', views.user_reg),
    path('users/login', views.user_login),
    path('logout', views.user_logout),
    path('signin', views.pg_signin),
    path('register', views.pg_register),
    path('dashboard', views.pg_dashboard),
    path('dashboard/admin', views.pg_dashboard_admin),
    path('users/new', views.pg_add),
    path('users/edit', views.pg_profile),
    path('users/edit/<int:id>', views.pg_edit_user),
    path('users/show/<int:id>', views.pg_show_user)
] 
