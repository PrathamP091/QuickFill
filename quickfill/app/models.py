from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES = (
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CH', 'Chandigarh'),
        ('CT', 'Chattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'J&K'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharastra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Orissa'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UT', 'Uttrakhand'),
        ('WB', 'West Bengal')
    )

CATEGORY_CHOICES=(
    ('petrol','Petrol'),
    ('diesel','Diesel'),
    ('engineoil','Engine-Oil'),
)

STATUS_CHOICES = {
    ('pending','Pending'),
    ('accepted','Accepted'),
    ('packed','Packed'),
    ('on the way','On The Way'),
    ('delivered','Delivered'),
    ('cancel','Cancel'),

}

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10, default="")
    subcategory = models.CharField(max_length=50, default="")
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="fuels", default="")
    stock_quantity = models.PositiveIntegerField(default=0)  # Add the stock_quantity field

    def save(self, *args, **kwargs):
        if not self.id:
            # Auto-generate the ID if it doesn't exist
            last_product = Product.objects.order_by('-id').first()
            if last_product:
                self.id = last_product.id + 1
            else:
                self.id = 1
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: {self.name}"

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.price

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.price
    
class Contact(models.Model) :
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    phone = models.CharField(max_length = 10)
    message = models.TextField(max_length = 500)
    def __str__(self):
        return self.name