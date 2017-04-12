from django.conf.urls import url
from django.contrib import admin
from posts import views

app_name    = 'posts'
urlpatterns = [
	url(r'^list/$', views.post_list, name="list"),
	url(r'^create/$', views.post_create, name="create"),
	url(r'^detail/(?P<id>[0-9]+)/$', views.post_detail, name="detail"),
	url(r'^update/$', views.post_update, name="update"),
	url(r'^delete/$', views.post_delete, name="delete"),

]