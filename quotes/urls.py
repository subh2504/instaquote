from django.urls import path
from django.contrib import admin

from .views import (
    post_list,
    PostLikedByAPIToggle,
    post_list_user,
    post_list_my,
    post_list_manage,
    post_create,
    post_detail,
    post_update,
    post_delete,
    post_deactivate,
    PostLikeToggle,
    PostLikeAPIToggle,
    )
app_name="quotes"
urlpatterns = [
    # url(r'^$', post_list, name='list'),
    # url(r'^create/$', post_create),
    # url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    # url(r'^(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
    # url(r'^api/(?P<slug>[\w-]+)/like/$', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    path(r'', post_list, name='list'),
    path('create/', post_create,name='create'),
    path('<int:pk>/', post_detail, name='detail'),
    path('<int:pk>/like/', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/<int:pk>/like/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('api/<int:pk>/likedby/', PostLikedByAPIToggle.as_view(), name='likedby-api-toggle'),

    path('<int:pk>/edit/', post_update, name='update'),
    path('<int:pk>/delete/', post_delete,name='delete'),
    path('<int:pk>/deactivate/', post_deactivate,name='deactivate'),
    path('u/<str:username>/', post_list_user,name='list_user'),
    path('mypost/', post_list_my,name='mypost'),
    path('manage/', post_list_manage,name='manage'),
    
]