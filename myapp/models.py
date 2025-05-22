from django.db import models

# Create your models here.


class user(models.Model):
    username=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    password=models.CharField(max_length=30)
    phone_number=models.IntegerField(blank=True,null=True)
    image=models.ImageField(upload_to="image",blank=True,null=True)
    otp=models.IntegerField(blank=True,null=True)


class category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name    
    
class product(models.Model):
    name=models.CharField(max_length=100)
    price = models.IntegerField()
    image=models.ImageField(upload_to="image")
    category=models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.name 


class wishlist(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class cart(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    total_price=models.IntegerField(default=1)

    added_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.qty})"


