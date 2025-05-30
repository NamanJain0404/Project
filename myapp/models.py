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
    order_status=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.qty})"

class Billing_details(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)

    def _str_(self):
        return f"{self.user.name} - {self.first_name} {self.last_name}"


class order(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    address = models.ForeignKey(Billing_details, on_delete=models.CASCADE)
    product = models.ManyToManyField(cart)
    subtotal=models.IntegerField()
    total=models.IntegerField()
    order_id=models.CharField(max_length=100)
    datetime=models.DateTimeField(auto_now_add=True)

    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

