from django.db import models
from brandsapp.models import Brand
from django.contrib.auth.models import User

# Create your models here.
class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Car name
    description = models.TextField()  # Detailed description
    quantity = models.PositiveIntegerField(default=0)  # Available stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='carsapp/uploads')
    def __str__(self):
        return self.name



class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Comments by {self.name}"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.car.name}"