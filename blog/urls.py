from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# namesapce = 'blog'

urlpatterns = [
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path('category/<int:id>/', views.post_category, name='post_category'),
    path('post/Tag/<int:id>/', views.post_Tag, name='post_Tag'),
    path('author/<int:id>/', views.post_author, name='post_author'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.post_list, name='post_list'),
    path('file_handling/', views.file_handling, name='file_handling'),
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
]