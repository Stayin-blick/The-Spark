from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create_post/', views.Create_Post.as_view(), name='create_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_details'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('user_profile/', views.UserProfile.as_view(), name='user_profile'),

]
