from django.shortcuts import render, get_object_or_404
from .models import Book, Quote

def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'journal/book.html', context)

def book_details(request, unique_id):
    book = get_object_or_404(Book, unique_id=unique_id)
    quotes = Quote.objects.filter(book=book)
    context = {
        'book': book,
        'quotes': quotes
    }
    return render(request, 'journal/book_details.html', context)
