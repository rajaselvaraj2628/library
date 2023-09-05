from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('members/', views.member_list, name='member_list'),
    path('issue/', views.issue_book, name='issue_book'),
    path('return/', views.return_book, name='return_book'),
    path('books/create/', views.create_book, name='create_book'),
    path('books/update/', views.update_book, name='update_book'),
    path('search-books/', views.search_books, name='search_books'),
    path('books/delete/', views.delete_book, name='delete_book'),
    path('members/create/', views.create_member, name='create_member'),
    path('members/update/', views.update_member, name='update_member'),
    path('members/delete/', views.delete_member, name='delete_member'),
    path('import-books/', views.book_import, name='book_import'),

]
