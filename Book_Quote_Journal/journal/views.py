from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from .models import Book, Quote
from .forms import BookForm, QuoteForm

def book_list(request):
    title = request.GET.get('title') if request.GET.get('title') != None else ''
    author = request.GET.get('author') if request.GET.get('author') != None else ''
    
    books = Book.objects.filter(
        Q(title__icontains = title),
        Q(author__name__icontains=author))

    books_titles = Book.objects.values_list('title', flat=True).distinct()
    books_authors = Book.objects.values_list('author__name', flat=True).distinct()


    context = {'books': books,
               'book_count': books.count(),
               'books_titles': books_titles,
               'books_authors': books_authors}
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
               'name': 'Book',
               'is_new': True,
               'action_type': 'Add'}
    return render(request, 'journal/book_form.html', context)

def createQuote(request,  unique_id):
    form = QuoteForm()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-details',  unique_id)
        
    context = {'form': form,
               'name': 'Quote',
               'is_new': True,
               'action_type': 'Add'}
    return render(request, 'journal/book_form.html', context)


def updateBook(request, unique_id):
    book = Book.objects.get(unique_id=unique_id)
    form = BookForm(instance=book)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-details',  unique_id=unique_id)

    context = {'form': form,
               'name': 'Book',
               'is_new': False,
               'action_type': 'Update'}
    return render(request, 'journal/book_form.html', context)

def updateQuote(request, unique_id):
    quote = Quote.objects.get(unique_id=unique_id)
    form = QuoteForm(instance=quote)

    if request.method == "POST":
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            return redirect('book-details', unique_id=quote.book.unique_id)
        
    context = {'form': form,
               'name': 'Quote',
               'is_new': False,
               'action_type': 'Update'}
    return render(request, 'journal/book_form.html', context)

def deleteBook(request, unique_id):
    book = Book.objects.get(unique_id=unique_id)
    book.delete()
    return redirect('book')

def deleteQuote(request, unique_id):
    quote = Quote.objects.get(unique_id=unique_id)
    quote.delete()
    return redirect('book-details', unique_id=quote.book.unique_id)