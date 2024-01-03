from django.urls import path
from .views import signup,home,login,logout,upload,likes,home_posts,explore,profile,follow,delete,search_results




urlpatterns = [
    path("",home),
    path("signup/",signup,name="signup"),
    path("login/",login,name="login"),
    path("logout/",logout,name="logout"),
    path('upload',upload,name='upload'),
    path('like-post/<str:id>',likes,name='like-post'),
    path('#<str:id>',home_posts),
    path('explore',explore),
    path('profile/',profile),
    path('follow',follow,name='follow'),
    path('delete/<str:id>',delete,name='delete'),
    path('search-results',search_results,name='search-results'),
]
