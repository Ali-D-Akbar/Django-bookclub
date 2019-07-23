from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from books.models import User, Book


class IndexView(generic.ListView):
    template_name = 'books/index.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """

        return Book.objects.order_by('-id')[:5]


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Book.objects


def login(request):
    if request.POST['username'] == '' or request.POST['password'] == '':
        return render(request, 'books/index.html', {
            'error_message': "You didn't enter text in a field.",
        })
    if User.objects.filter(username__iexact=request.POST['username'], password=request.POST['password']).exists():
        return HttpResponse("You have successfully logged in!")
    else:
        return render(request, 'books/index.html', {
            'error_message': "USERNAME/PASSWORD MISMATCH.",
        })


def signup(request):
    if request.POST['username'] == '' or request.POST['password'] == '' or request.POST['email'] == '':
        return render(request, 'books/index.html', {
            'error_message': "You didn't enter text in a field.",
        })
    user = User(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
    user.save()
    return HttpResponse("You have successfully signed up!")


def home(request):
    return HttpResponse("Home Page!")
