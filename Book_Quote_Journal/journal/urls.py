from django.urls import path
from . import views

urlpatterns = [
    path('', views.book, name = 'book'),
    path('book_details/', views.book_details, name='details')
]