from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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

@login_required(login_url='book')
def book_details(request, unique_id):
    book = get_object_or_404(Book, unique_id=unique_id)
    quotes = Quote.objects.filter(book=book)
    context = {
        'book': book,
        'quotes': quotes,
        'unique_id': unique_id
    }
    return render(request, 'journal/book_details.html', context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('book')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'journal/login_register.html', {'page': 'login'})


def logoutPage(request):
    logout(request)
    return redirect('book')

def signupPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('book')

    context = {'form': form}
    return render(request, 'journal/login_register.html', context)

@login_required(login_url='book')
def createBook(request):
    form = BookForm()

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('book')

    context = {'form': form,
               'name': 'Book',
               'is_new': True,
               'action_type': 'Add'}
    return render(request, 'journal/book_form.html', context)

@login_required(login_url='book')
def createQuote(request,  unique_id):
    book = Book.objects.get(unique_id=unique_id)
    form = QuoteForm(initial={'book': book})

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('book-details',  unique_id)
        
    context = {'form': form,
               'name': 'Quote',
               'is_new': True,
               'action_type': 'Add'}
    return render(request, 'journal/book_form.html', context)

@login_required(login_url='book')
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

@login_required(login_url='book')
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

@login_required(login_url='book')
def deleteBook(request, unique_id):
    book = Book.objects.get(unique_id=unique_id)
    book.delete()
    return redirect('book')

@login_required(login_url='book')
def deleteQuote(request, unique_id):
    quote = Quote.objects.get(unique_id=unique_id)
    quote.delete()
    return redirect('book-details', unique_id=quote.book.unique_id)