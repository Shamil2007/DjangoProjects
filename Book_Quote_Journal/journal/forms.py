from django.forms import ModelForm
from .models import Book, Quote


class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ['user']  

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        exclude = ['user']  #
