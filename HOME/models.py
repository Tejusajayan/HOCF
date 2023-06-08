from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.
class food(models.Model):
    foodname=models.CharField(max_length=40)
    foodprice=models.PositiveIntegerField()
    cate=models.CharField(max_length=30)
    foodimg=models.ImageField(upload_to='FOODS')
    special=models.BooleanField(default=False)
    avai=models.BooleanField(default=True)

    def __str__(self):
        return self.foodname

class review(models.Model):
    name=models.CharField(max_length=20)
    content=models.TextField()

    def __str__(self):
        return self.name

class order(models.Model):
    name=models.CharField(_("Customer Name"),max_length=20,blank=False,null=False)
    amount=models.FloatField(_("Amount"),null=False,blank=False)
    status=models.CharField(
        _("Payment Status"),
        default="PENDING",max_length=254,null=False,blank=False
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )
    is_paid=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}-{self.provider_order_id}"

class customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class cartitem(models.Model):
    order=models.ForeignKey(customer,on_delete=models.SET_NULL,blank=True,null=True)
    product=models.ForeignKey(food,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    orderid=models.CharField(max_length=10)

    def __str__(self):
        return self.orderid
    
    
class finalord(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.SET_NULL,blank=True,null=True)
    transaction_id=models.PositiveIntegerField(default=0)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    bill=models.PositiveIntegerField(default=0)
    payment=models.CharField(max_length=30)
    paymentid=models.CharField(default='-',max_length=50)
    paydone=models.BooleanField(default=False)
    name=models.CharField(max_length=30)
    number=models.PositiveBigIntegerField(default=0)
    doorno=models.CharField(max_length=200)
    landmark=models.CharField(max_length=100)
    pincode=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class dinereq(models.Model):
    name=models.CharField(max_length=20)
    number=models.PositiveBigIntegerField()
    datetime=models.DateTimeField()
    seat=models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name



