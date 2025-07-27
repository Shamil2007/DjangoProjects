from django.forms import ModelForm
from .models import Book, Quote


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = '__all__'