from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),    path('accounts/profile/', views.profile_redirect_view, name='profile_redirect'),
    path('add_post/', views.add_post, name='add_post'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('feed/', views.feed_view, name='feed'),

]
