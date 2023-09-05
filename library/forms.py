from django import forms
from .models import Book, Member

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'quantity', 'isbn']

class BookImportForm(forms.Form):
    title = forms.CharField(label='Title', required=False)
    authors = forms.CharField(label='Authors', required=False)
    isbn = forms.CharField(label='ISBN', required=False)
    publisher = forms.CharField(label='Publisher', required=False)
    page = forms.IntegerField(label='Page', required=False)
    num_books = forms.IntegerField(label='Number of Books to Import', min_value=1)

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone']

class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'quantity', 'isbn']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['isbn'].widget.attrs.update({'class': 'form-control'})
class IssueBookForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.all())
    book = forms.ModelChoiceField(queryset=Book.objects.filter(is_issued=False))

class DeleteMemberForm(forms.Form):
    member_name = forms.CharField(max_length=100, label='Member Name')

class ReturnBookForm(forms.Form):
    member_id = forms.IntegerField(label='Member ID')
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label=None)
    rental_fee = forms.DecimalField(max_digits=6, decimal_places=2, required=True)

class UpdateMemberForm(forms.Form):
    member_identifier = forms.CharField(max_length=100, required=True, label='Member Name or Unique Identifier')
    new_email = forms.EmailField(max_length=100, required=False, label='New Email Address')

class BookSearchForm(forms.Form):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)