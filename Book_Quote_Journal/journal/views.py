from django.shortcuts import redirect, render, get_object_or_404
from .models import Book, Quote
from .forms import BookForm, QuoteForm

def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'journal/book.html', context)

def book_details(request, unique_id):
    book = get_object_or_404(Book, unique_id=unique_id)
    quotes = Quote.objects.filter(book=book)
    context = {
        'book': book,
        'quotes': quotes,
        'unique_id': unique_id
    }
    return render(request, 'journal/book_details.html', context)

def createBook(request):
    form = BookForm()

    if request.method == "POST":
        print(request.POST)
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book')

    context = {'form': form,
               'name': 'Book'}
    return render(request, 'journal/book_form.html', context)

def createQuote(request,  unique_id):
    form = QuoteForm()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-details',  unique_id)
        
    context = {'form': form,
               'name': 'Quote'}
    return render(request, 'journal/book_form.html', context)