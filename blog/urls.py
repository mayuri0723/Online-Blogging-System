from django.urls import path
from . import views


urlpatterns = [
     path("", views.home, name='home'),
     path("about/", views.about, name='about'), 
     path("contact/", views.contact, name='contact'),  
     path("dashboard/", views.dashboard, name='dashboard'), 
     path("signup/", views.user_signup, name='signup'),  
     path("login/", views.user_login, name='login'), 
     path("logout/", views.user_logout, name='logout'),
     path("addpost/", views.add_post, name='addpost'),   
     path("updatepost/<int:id>/", views.update_post, name='updatepost'),
     path("delete/<int:id>/", views.delete_post, name='deletepost'),
     path("post_detail/<int:pk>/", views.add_comment_to_post ,name='post_detail'),
     path("add_comment_to_post/<int:pk>/", views.add_comment_to_post ,name='add_comment'),
     path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
     path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
     path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
     path('search/', views.search, name="search"),
     
]
