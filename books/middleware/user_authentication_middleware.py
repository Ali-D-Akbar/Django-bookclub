from django.shortcuts import get_object_or_404, render

from books.models import Book


class UserAuthenticationMiddleware(object):
    def process_request(self, request):
        book = get_object_or_404(Book, pk=request.POST['book_id'])
        if request.user != book.user:
            error_message = 'You are not allowed to edit. Please Login again. '
            return render(request, 'books/edit.html', {'error_message': error_message})


class SuperUserAuthenticationMiddleware(object):
    def process_request(self, request):
        try:
            if not request.user.is_superuser:
                error_message = 'You are not allowed to add Bulk Data because you are not a Super User!'
                return render(request, 'books/add_bulk.html', {'error_message': error_message})
        except AttributeError:
            error_message = "You are not allowed to add Bulk Data because you are not a Super User!"
            return render(request, 'books/index.html', {'error_message': error_message})

