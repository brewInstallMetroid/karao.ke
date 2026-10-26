from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello, name='home'),
    path('hello/', views.hello, name='hello'),
    path('recent/record/', views.record_recent_song, name='record_recent_song'),
    path('recent/clear/', views.clear_recent, name='clear_recent'),
]
