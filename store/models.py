from django.db import models

# Create your models here.

class Collection(models.Model):

    title = models.CharField(max_length=255)



class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    featured_product = models.ForeignKey('Product' , on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    # by default django create primary key for each class --> id but if i intialize one it does not crete --> id
    # sku = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField() 
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now= True)
    collection = models.ForeignKey(Collection , on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    
    M_BRONZE = 'B'
    M_SILVER = 'S'
    M_GOLD = 'G'

    MEMBERSHIP_CHOICES = {
        (M_BRONZE , 'Bronze'),
        (M_SILVER , 'Silver'),
        (M_GOLD , 'Gold'),
    }
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255 , unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1 ,choices=MEMBERSHIP_CHOICES , default=M_BRONZE)



class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add = True)

    PAYMENT_CHOICES = {
        ('P' , 'Pending'),
        ('C' , 'Complete'),
        ('F' , 'Failed')
    }

    payment_status = models.CharField(max_length=1 , choices=PAYMENT_CHOICES)
    customer = models.ForeignKey(Customer , on_delete=models.PROTECT)



class OrderItem(models.Model):

    order =  models.ForeignKey(Order , on_delete=models.PROTECT)
    product =  models.ForeignKey(Product , on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6 , decimal_places=2)



class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    
# one to one relationship
    customer = models.OneToOneField(Customer , on_delete=models.CASCADE, primary_key=True)
# one to many relationship
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)

    

class Cart(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
#   here if we delete cart it delete associate items

    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

