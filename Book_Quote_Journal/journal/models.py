import random
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    birthday = models.DateField()

    def __str__(self):
        return self.name
    

class Genre(models.Model):
    genre = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.genre

def generate_unique_id():
    return random.randint(1000, 9999)

class Book(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    page = models.IntegerField(null=True, blank=True, 
                               validators=[MinValueValidator(0), MaxValueValidator(2000)])
    created_date = models.DateTimeField(auto_now_add=True)
    unique_id = models.IntegerField(default=generate_unique_id, 
                                    unique=True, blank=True, 
                                    null=True, editable=False)

    def __str__(self):
        return self.title
    





class Quote(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(max_length=500, null=False, blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(2000)])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name