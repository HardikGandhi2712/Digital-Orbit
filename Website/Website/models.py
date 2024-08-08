from django.db import models

class product(models.Model):
    pid=models.IntegerField(primary_key=True)
    pname=models.CharField(max_length=100)
    Sdescription=models.CharField(max_length=100)
    Ldescription=models.CharField(max_length=100)
    price=models.IntegerField()
    category=models.CharField(max_length=20)
    photo1=models.ImageField()
    photo2=models.ImageField()
    photo3=models.ImageField()

    class Meta:
        db_table="product"


class customer(models.Model):
    email=models.CharField(max_length=30,primary_key=True)
    cname=models.CharField(max_length=15)
    contact=models.BigIntegerField()
    pass1=models.CharField(max_length=15)
    
    class Meta:
        db_table="customer"


class feed(models.Model):
    cname=models.CharField(max_length=20)
    email=models.CharField(max_length=30,primary_key=True)
    feedback=models.CharField(max_length=15)

    class Meta:
       db_table="feed"


class cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=15)
    price = models.IntegerField()
    pid = models.IntegerField()
    email=models.CharField(max_length=30)

    class Meta:
        db_table = "cart"


class bill(models.Model):
    bill_id= models.AutoField(primary_key=True)
    address=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    payment=models.CharField(max_length=15)
    pname = models.CharField(max_length=15)
    price = models.IntegerField()
    pid = models.IntegerField()
    uni = models.CharField(max_length=50)

    class Meta:
        db_table = "bill"