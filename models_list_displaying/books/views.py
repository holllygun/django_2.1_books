import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from datetime import date
from books.models import Book
from books.converters import DateConverter

def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)



def book(request, pub_date):
    books = Book.objects.all().order_by('pub_date')
    b_pages = [c.pub_date for c in books]
    conv = DateConverter()
    b_dict = {}
    count = 1
    for page in b_pages:
        page = conv.to_url(page)
        b_dict[page] = count
        count += 1
    info = []
    for book in books:
        info.append({
            'name': book.name,
            'author': book.author,
            'pub_date': book.pub_date,
        })
    paginator = Paginator(info, 1)
    page_number = int(request.GET.get("page", b_dict[pub_date]))
    page = paginator.get_page(page_number)
    template = 'books/book.html'
    context = {
        'book': info[page_number-1],
        'page': page,
               }
    return render(request, template, context)
