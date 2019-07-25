from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import generic

from books.models import Book


class IndexView(generic.ListView):
    template_name = 'userauth/index.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """

        return Book.objects.order_by('-id')[:5]


def login(request):
    if request.POST['username'] == '' or request.POST['password'] == '':
        return render(request, 'userauth/index.html', {
            'error_message': "You didn't enter text in a field.",
        })
    if User.objects.filter(username__iexact=request.POST['username'], password=request.POST['password']).exists():
        request.session['username'] = request.POST['username']
        return redirect('books:index')
    else:
        return render(request, 'userauth/index.html', {
            'error_message': "USERNAME/PASSWORD MISMATCH.",
        })


def signup(request):
    if request.POST['username'] == '' or request.POST['password'] == '' or request.POST['email'] == '':
        return render(request, 'userauth/index.html', {
            'error_message': "You didn't enter text in a field.",
        })
    if User.objects.filter(username__iexact=request.POST['username']).exists():
        return render(request, 'userauth/index.html', {
            'error_message': "This username already exists. Please change the username and try again",
        })
    user = User(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
    user.save()
    request.session['username'] = request.POST['username']
    return redirect('books:index')


def logout(request):
    request.session['username'] = False
    return redirect('books:index')
