from django.contrib.auth.decorators import login_required
import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from books.forms import AddBookForm
from books.middleware.user_authentication_middleware import UserAuthenticationMiddleware, \
    SuperUserAuthenticationMiddleware
from books.models import Book
from django.utils.decorators import decorator_from_middleware

from userauth.models import Profile


@decorator_from_middleware(UserAuthenticationMiddleware)
def edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/edit.html', {'book': book})


def update_book(request, pk):
    if request.method == "POST":
        book = get_object_or_404(Book, id=pk)
        if book is not None:
            book.title = request.POST.get('title')
            book.author = request.POST.get('author')
            book.description = request.POST.get('description')
            book.save()
            return redirect(reverse('books:detail', args=[pk]))
    else:
        return redirect('books:index')


@login_required
def add_book(request):
    add_book_form = AddBookForm(data=request.POST)
    if add_book_form.is_valid():
        profile = Profile.objects.get(user=request.user)
        book = add_book_form.save()
        book.user_id = profile.id
        book.save()
        return redirect('books:add_book')
    else:
        add_book_form = AddBookForm()
    return render(request, 'books/add_book.html', {'add_book_form': add_book_form})


@decorator_from_middleware(SuperUserAuthenticationMiddleware)
def add_bulk(request):
    if request.POST:
        bulk_books = request.POST['json_bulk_data']
        for deserialized_object in serializers.deserialize("json", bulk_books):
            deserialized_object.save()
        return HttpResponse("Data has been saved from the JSON file.")
    else:
        return render(request, 'books/add_bulk.html')


def detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book': book})


class IndexView(generic.ListView):
    template_name = 'books/index.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        """
        Return the last five published Books
        """

        return Book.objects.order_by('-id')[:5]
