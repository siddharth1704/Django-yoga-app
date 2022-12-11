from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("classes/", views.all_classes, name="all"),
    path("book/", views.book, name='book'),
    path("logout/", views.logout, name='logout'),
    path("login/", views.login, name='login')
]
