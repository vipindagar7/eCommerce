from django.db import models
from accounts.models import SellerProfile , CustomUser
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

    
class Product(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    image1 = models.ImageField( upload_to='media/product_images')
    image2 = models.ImageField( upload_to='media/product_images',null=True , blank=True)
    image3 = models.ImageField( upload_to='media/product_images',null=True , blank=True)
    image4 = models.ImageField( upload_to='media/product_images',null=True , blank=True)
    image5 = models.ImageField( upload_to='media/product_images',null=True , blank=True)
    video = models.FileField( upload_to='media/product_videos',null=True , blank=True)
    name = models.CharField( max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ManyToManyField(Category)
    color = models.TextField()
    size = models.TextField()
    conditions = models.TextField()
    brand = models.CharField( max_length=250)
    quantity = models.IntegerField()
    def __str__(self):
        return str(self.seller.user.email) + " , " + str(self.name)
    
    




class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    added_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE )
    address = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Override the save method to update product quantities when an order item is saved
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.quantity -= self.quantity
        self.product.save()

    # Override the delete method to restore product quantities when an order item is deleted
    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)