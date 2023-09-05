from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    isbn = models.CharField(max_length=13)
    is_issued = models.BooleanField(default=False)
    issue_to = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    rental_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    issued_books = models.ManyToManyField(Book, related_name='members_issued', blank=True)
    
    def __str__(self):
        return self.name
class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.book.title} - {self.member.name}"
