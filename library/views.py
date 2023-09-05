from datetime import date

from django.core.exceptions import ObjectDoesNotExist
import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Member, Issue
from .forms import BookSearchForm, BookForm, MemberForm, IssueBookForm, ReturnBookForm, UpdateMemberForm, \
    UpdateBookForm, BookImportForm
from django.contrib import messages

def home(request):
    return render(request, 'library/home.html')  # Replace 'home.html' with your actual template name
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})
def member_list(request):
    members = Member.objects.all()
    return render(request, 'library/member_list.html', {'members': members})
def issue_book(request):
    if request.method == 'POST':
        member = request.session.get('name')
        book_title= request.session.get('title')

        try:
            member = Member.objects.get(id=member)
            book = Book.objects.get(id=book_title)

            if book.issued_to == member:
                messages.error(request, 'This book is already issued to the member.')
            else:
                book.issued_to = member
                book.save()
                request.session.pop('member_id')
                request.session.pop('book_id')

                messages.success(request, 'Book issued successfully.')

        except Member.DoesNotExist:
            messages.error(request, 'Member not found.')
        except Book.DoesNotExist:
            messages.error(request, 'Book not found.')

    return render(request, 'library/issue_book.html')
    # return redirect('library/book_list')

def return_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('title')
        member_id = request.POST.get('name')

        try:

            book = Book.objects.get(pk=book_id)
            member = Member.objects.get(pk=member_id)


            rent_fee = calculate_rent_fee(book)

            # Check if the member's outstanding debt exceeds Rs. 500
            if member.outstanding_debt + rent_fee > 500:
                messages.error(request, 'Outstanding debt exceeds Rs. 500. Cannot return the book.')
            else:
                member.outstanding_debt += rent_fee
                member.save()

                book.returned = True
                book.save()

                messages.success(request, 'Book Returned successfully.')
                return render(request, 'library/book_list.html')

        except Book.DoesNotExist:
            messages.error(request, 'Book not found.')
        except Member.DoesNotExist:
            messages.error(request, 'Member not found.')

    return render(request, 'library/return_book.html')
def calculate_rent_fee(book):
    issue_date = book.issue_date
    due_date = book.due_date
    today = date.today()
    duration = (today - issue_date).days
    rent_fee = duration * 10
    return rent_fee
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:book_list')
    else:
        form = BookForm()

    return render(request, 'library/create_book.html', {'form': form})

def search_books(request):
    if request.method == 'GET':
        form = BookSearchForm(request.GET)
        if form.is_valid():
            book_name = form.cleaned_data.get('book_name')
            author = form.cleaned_data.get('author')

            books = Book.objects.all()

            if book_name:
                books = books.filter(title__icontains=book_name)
            if author:
                books = books.filter(author__icontains=author)

            return render(request, 'library/search_books.html', {'books': books, 'form': form})

    form = BookSearchForm()
    return render(request, 'library/search_books.html', {'form': form})

def update_book(request):
    if request.method == 'POST':
        form = UpdateBookForm(request.POST)
        if form.is_valid():
            book_id = request.POST.get('title')

            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return render(request, 'library/book_not_found.html')

            # Update the book's information based on the form data
            book.title = form.cleaned_data['title']
            book.author = form.cleaned_data['author']
            book.quantity = form.cleaned_data['quantity']
            book.isbn = form.cleaned_data['isbn']

            book.save()

            return redirect('library:book_list')
    else:
        form = UpdateBookForm()

    return render(request, 'library/update_book.html', {'form': form})
def delete_book(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        title = request.POST.get('title')

        try:
            book = Book.objects.get(isbn=isbn, title=title)
            book.delete()
            return redirect('library:book_list')
        except Book.DoesNotExist:
            return render(request, 'library/book_not_found.html')

    return render(request, 'library/delete_book.html')
def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:member_list')
    else:
        form = MemberForm()

    return render(request, 'library/create_member.html', {'form': form})

def update_member(request):
    if request.method == 'POST':
        form = UpdateMemberForm(request.POST)
        if form.is_valid():
            member_identifier = form.cleaned_data['member_identifier']

            try:
                member = Member.objects.get(name=member_identifier)

                new_email = form.cleaned_data['new_email']
                member.email = new_email
                member.save()

                return redirect('library:member_list')
            except Member.DoesNotExist:
                return render(request, 'library/member_not_found.html')

    else:
        form = UpdateMemberForm()

    return render(request, 'library/update_member.html', {'form': form})
def book_import(request):
    if request.method == 'POST':
        form = BookImportForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            authors = form.cleaned_data['authors']
            isbn = form.cleaned_data['isbn']
            publisher = form.cleaned_data['publisher']
            page = form.cleaned_data['page']
            num_books = form.cleaned_data['num_books']

            api_url = 'https://frappe.io/api/method/frappe-library'

            params = {
                'title': title,
                'authors': authors,
                'isbn': isbn,
                'publisher': publisher,
                'page': page,
                'num_books': num_books,
            }

            response = requests.get(api_url, params=params)

            if response.status_code == 200:
                data = json.loads(response.text)

                for book_data in data.get('message', []):
                    isbn = book_data.get('isbn')
                    title = book_data.get('title')
                    authors = book_data.get('authors')

                    try:
                        existing_book = Book.objects.get(isbn=isbn)  # Check if book with ISBN exists
                        existing_book.title = title
                        existing_book.authors = authors
                        existing_book.save()
                    except Book.DoesNotExist:
                        new_book = Book(title=title, authors=authors, isbn=isbn,)
                        new_book.save()

                messages.success(request, 'Books imported successfully')
                return render(request, 'library/book_import.html')  # Redirect back to the import page
            else:
                messages.error(request, 'Failed to import books')

    else:
        form = BookImportForm()

    return render(request, 'library/import_books.html', {'form': form})

def delete_member(request):
    if request.method == 'POST':
        member_name = request.POST.get('member_name')

        try:
            member = Member.objects.get(name=member_name)
            member.delete()  # Delete the book
            return redirect('library:member_list')  # Redirect to the book list page after deletion
        except Member.DoesNotExist:
            return render(request, 'library/member_not_found.html')

    return render(request, 'library/delete_member.html')  # Render the delete book form
