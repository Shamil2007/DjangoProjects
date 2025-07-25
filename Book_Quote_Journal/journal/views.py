from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def book(request):
    return HttpResponse("The book page")

def book_details(request):
    return HttpResponse("The details are")