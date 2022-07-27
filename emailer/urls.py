from django.urls import path

from emailer import views

urlpatterns = [
    path('', views.send)
]
