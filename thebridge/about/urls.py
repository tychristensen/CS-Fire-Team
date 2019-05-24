from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('user', views.user, name='user'),
	path('officer', views.officer, name='officer'),
	path('admin', views.admin, name='admin'),
]
