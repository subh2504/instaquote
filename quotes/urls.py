from django.urls import path
from django.contrib import admin

from .views import (
    post_list,
    post_list_user,
    post_create,
    post_detail,
    post_update,
    post_delete,
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
    path('create/', post_create),
    path('<int:pk>/', post_detail, name='detail'),
    path('<int:pk>/like/', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/<int:pk>/like/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('<int:pk>/edit/', post_update, name='update'),
    path('<int:pk>/delete/', post_delete),
    path('u/<str:username>/', post_list_user,name='list_user'),
]