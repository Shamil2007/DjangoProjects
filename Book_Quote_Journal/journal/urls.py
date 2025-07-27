from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name = 'book'),
    path('book_details/<int:unique_id>/', views.book_details, name='book-details'),

    path('createBook/', views.createBook, name='createBook'),
    path('<int:unique_id>/updateBook/', views.updateBook, name='updateBook'),

    path('book_details/<int:unique_id>/createQuote', views.createQuote , name = 'createQuote'),
    path('quote/<int:unique_id>/update/', views.updateQuote, name='updateQuote')

    
]