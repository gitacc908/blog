from django.urls import path
from . import views


urlpatterns = [
	path('blogs/', views.allblog, name='blogs'),
	path('blogs/create/', views.create_post, name='create_post'),
	path('blog_detail/<str:slug>/', views.allblog, name='detail'),
	path('tags/', views.tags, name='tags'),
	path('tags/create/', views.create_tag, name='create_tag'),
	path('tags/<str:slug>/update/', views.tag_update, name='tag_update'),
	path('tags/<str:slug>/delete/', views.tag_delete, name='tag_delete'),
	path('blog_detail/<str:slug>/delete/', views.blog_delete, name='blog_delete'),
	path('blogs/<str:slug>/update/', views.blog_update, name='blog_update'),
	path('tags/<str:slug>/', views.tags, name='tag_detail'),
]
