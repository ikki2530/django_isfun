from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    # Acustomer can have one user, and a user can have one customer, blank means it not must be associated to a user
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone= models.CharField(max_length=200)
    email= models.CharField(max_length=200)
    profile_pic = models.ImageField(default="profile.jpeg",null=True, blank=True) # add pillow library,
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )

    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(max_length=200, choices=CATEGORY)
    description = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    # SET_NULL
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL) 
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL) 
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS)

    def __str__(self):
        return self.product.name
    
