from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Collection(models.Model):
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    featured_product = models.ForeignKey('Product' , on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    # by default django create primary key for each class --> id but if i intialize one it does not crete --> id
    # sku = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True) 
    unit_price = models.DecimalField(
        max_digits=6 ,
        decimal_places=2,
        validators=[MinValueValidator(1)]
        )
    inventory = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    last_update = models.DateTimeField(auto_now= True)
    collection = models.ForeignKey(Collection , on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class Customer(models.Model):
    
    M_BRONZE = 'B'
    M_SILVER = 'S'
    M_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (M_BRONZE , 'Bronze'),
        (M_SILVER , 'Silver'),
        (M_GOLD , 'Gold'),
    ]
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255 , unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1 ,choices=MEMBERSHIP_CHOICES , default=M_BRONZE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name','last_name']

    # expected as reverse relationship field 'order_set' but it is 'order'
    
    # class Meta:
    #     db_table = 'store_customer' #not recommended
    #     indexes = [
    #         models.Index(fields=['last_name','first_name'])
    #     ]


class Order(models.Model):

    PAYMENT_CHOICES = [
        ('P' , 'Pending'),
        ('C' , 'Complete'),
        ('F' , 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add = True)
    payment_status = models.CharField(max_length=1 , choices=PAYMENT_CHOICES)
    
    customer = models.ForeignKey(Customer , on_delete=models.PROTECT)



class OrderItem(models.Model):
    # so django create reverse ralationship with column 'orderitem_set' you can change the name if you add related_name attr to the relation
    order =  models.ForeignKey(Order , on_delete=models.PROTECT)
    
    product =  models.ForeignKey(Product , on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6 , decimal_places=2)



class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10 , null=True , blank=True)

# one to one relationship
    # customer = models.OneToOneField(Customer , on_delete=models.CASCADE, primary_key=True)
# one to many relationship
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)

    

class Cart(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
#   here if we delete cart it delete associate items

    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

