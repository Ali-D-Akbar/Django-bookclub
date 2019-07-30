from django.http import HttpResponse
from django.views import generic
from books.models import Book


class IndexView(generic.ListView):
    template_name = 'books/index.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """

        return Book.objects[:5]


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'
