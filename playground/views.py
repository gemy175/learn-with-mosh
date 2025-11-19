from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count , Max, Min, Avg, Sum
from store.models import Product, OrderItem, Order, Customer

def say_hello(req):
    # every object has attribute called 'objects' which returns a 'manager' 
    # and that 'manager' is the interface to the DATABASE
    # 'manager' has some methods for quering and updating data most of this methods(all , filter,...) return QUERY SET 
    # .. some methods return the result immediatly (count , get, ..)
    
    # QUERY SET
    # this return query set -> it is an object that encapsulate a query 
    #.. that is implemented at some point when used (in multiple scenarios)
    
    # query_set = Product.objects.all()
    
    #  scenario 1
    # for product in query_set:
    #     print(product)

    #  scenario 2
    # list(query_set)

    #   scenario 2
    # query_set[0]
    # query_set[0:5]
    # --------->> thats why the Query set is lazy as it is evaluated at later point
    # ->>why that ? >> as it used in complex queries
    #   ***complex query example*****
    # query_set.filter().filter().order_by()

    # METHODS 
    # all() -> return Query Set
    # get() , get(pk=1) pk is translated to the primary key attribute name in the target object (it is existed with other methods than get)
    # get() -> return actual object 
    # so problems in this code:
    #   using get with not existed pk number gives error in page
    #   so you use try catch (but deos this proffesional or there is way "line 45")
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass

    # here if pk not exist it would return None (not error)
    # product = Product.objects.filter(pk=0).first()
    # exists return boolean
    # exists = Product.objects.filter(pk=0).exists()
    # *******************************************************************
    # # ******* FILTER with LOOK UP TYPES return query set *********
    # *******************************************************************
    # # filter based on field vlaue
    # queryset = Product.objects.filter(unit_price__lt=20)
    # queryset = Product.objects.filter(unit_price__lte=20)
    # queryset = Product.objects.filter(unit_price__gt=20)
    # queryset = Product.objects.filter(unit_price__gte=20)

    # # filter based on field vlaues range
    # queryset = Product.objects.filter(unit_price__range=(20, 30))

    # # filter based on relationships
    # queryset = Product.objects.filter(collection__id=1)
    # #                               we can also add look up types
    # queryset = Product.objects.filter(collection__id__lt=1)
    # queryset = Product.objects.filter(collection__id__range=(1,10))

    # # filter based on strings
    # queryset = Product.objects.filter(title__contains='coffee') #case sensitive
    # queryset = Product.objects.filter(title__icontains='coffee') #case unsensitive
    # queryset = Product.objects.filter(title__startswith='coffee') #startswith case unsensitive
    
    # # filter based on date
    # queryset = Product.objects.filter(last_update__year=2021) 
    # queryset = Product.objects.filter(last_update__month=10) #and also could be day 
    # # find null values
    # queryset = Product.objects.filter(description__isnull=True) 


    # # **************** how to make AND ************
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20) #1
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20) #2

    # # Q()
    # # **************** what about OR or NOT how to implement them ***********
    # #                   solution is -->> Q()
    # #                                                     OR                    
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)) 
    # #                                                   AND, NOT operator 
    # queryset = Product.objects.filter (Q(inventory__lt=10) & ~Q(unit_price__lt=20))


    # # F()
    # # ************** referencing fields using F() *********
    # # like if we get product that it's inventory = unit_price

    # queryset = Product.objects.filter (inventory = F('unit_price'))
    
    # # we can also reference a field in related table 
    # queryset = Product.objects.filter (inventory = F('collection__id'))
    
    
    # # ************************************************************
    # #                       SORTING
    # # ************************************************************
    # # order by return query set 
    # queryset = Product.objects.order_by('title') #order ascending
    # queryset = Product.objects.order_by('-title') #order descending
    # queryset = Product.objects.order_by('unit_price','-title') #ordering based on 2 fields
    # # reverse(), order by() is one of query set mehtods so every thing return QS could run one of this mehtod on it 
    # queryset = Product.objects.order_by('unit_price','-title').reverse()
    
    # queryset = Product.objects.filter(collection__id=1).order_by('unit_price') #filter then order
    # # this return product not query set 
    # product = Product.objects.order_by('unit_price')[0] #order then slice the first element
    # # we can do the same with earliest function
    # product = Product.objects.earliest('unit_price') # it sort in ascening and get the first element
    # product = Product.objects.latest('unit_price') # it sort in descening and get the last element
    # # earliest and latest return object
    # # order by return query set 


    
    # # ************************************************************
    # #                       LIMITING RESULTS
    # # ************************************************************
    # query_set = Product.objects.all()[:5] # return 0 -> 5
    # query_set = Product.objects.all()[5:10] # return 5 -> 9

    
    # # ************************************************************
    # #                      selecting fields to QUERY
    # # ************************************************************

    # # how to query specific fields -->> values() , values_list()
    # # values() --->> (query set) return list of dictionaries 
    # # values_list() --->> (query set) return list of tuples
    
    # queryset = Product.objects.values('id', 'unit_price')
    # queryset = Product.objects.values('id', 'unit_price','collection__id') #could also contain field in related data
    # queryset = Product.objects.values_list('id', 'unit_price','collection__id') #could also contain field in related data
    # # values return Query set so we can implement distinct() on it 
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')

    # # ************************************************************
    # #                   Deferring Fields
    # # ************************************************************
    # # only() -> specify the fields we want to read from the database
    # # how it different from values() ?? -> 
    # # only -> instances of Product class 
    # # values -> dictionary objects
    # queryset = Product.objects.only('id', 'title')
    # # must be carefull when using the 'only' mehtod to avoid extra queries -> like if you added another field(in rendering) not specified in only() it would make extra query for each object 
    # # defer() is the opposit to only 
    # queryset = Product.objects.defer('description')

    # ************************************************************
    #                   Select Related Object
    # ************************************************************
    # use 'select_related()' when other end of relationship has one instance
    # use 'prefetch_related()' when other end of relationship has many instances
    # both return a Query Set
    # all() only reload the object (Product) but if in render we used a field in related table django will do SQL query for each product (overhead)
    # queryset = Product.objects.all() 
    # how to load related objects also """select_related('field to preload')"" then all()
    # queryset = Product.objects.select_related('collection').all() 
    # we could also span relationships so if collection have relation with other table on field "f1" we could do so 
    # queryset = Product.objects.select_related('collection__f1').all() 

    # prefetch_related()
    # queryset = Product.objects.prefetch_related('promotions').all() 

    # we can also use them together 
    # queryset = Product.objects.prefetch_related('promotions').select_related('collection').all() 
    

    # ******************************************
        #   TASK
    # ******************************************
    # 'order' object do not has relationship with product and we want to extract order with its products ...??
    # but 'order' has relation to 'orderItem' object which has relation to products so we reach product through it 
    # order (1) -> (n) order_item so we put the field in orderItem but django create the reverse relationship with name 'orderitem_set'
    #so we can use it to relate to orderItem object and through it to 'product' object

    # orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5] 



    # # ******************************************
    #     #   Agreggating Objects
    # # ******************************************
    # # aggregate is one of query set methods 
    # result = Product.objects.aggregate(Count('id')) # return dictionary # better to use the pk field # it name the dict output 'id' in used this case {id__count} 
    # result = Product.objects.aggregate(count=Count('id')) #this change the name in output dictionary to count

    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    # result = Product.objects.filter(collection__id=1).aggregate(count=Count('id'), min_price=Min('unit_price'))


    # ******************************************
        #   Annotate Objects
    # ******************************************

    # sometimes we need to add additional attributes to our objects while quering them 
    # queryset = Customer.objects.annotate(is_new=True) # ERROR -> as annotate() take only Expression
    #Expression class is the base class for all classes/types of expression --> value > (num , bool , str) , f > (field in same or other table) , func >(DB functions) , aggregate > (aggregate classes)
    
    #      ******** value() ******                                                                 
    queryset = Customer.objects.annotate(is_new=Value(True))
    
    #      ******** F() ******                                                                 
    # can we assign the value compared to a value related to other field ???
    # yep , f() 
    queryset = Customer.objects.annotate(new_id=F('id'))
    queryset = Customer.objects.annotate(new_id=F('id') + 1)

    #      ******** Func() ****** 
    # database funcitons
    # 'CONCAT'                                          
    queryset = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
    # there is short-hand to achive concat no F() but need value(' ') otherwise django will think ' ' is column in table
    queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))

    #      ******** Grouping Data****** 

    queryset = Customer.objects.annotate(
        order_count=Count('order')
    )

    #      ******** Working with Expression Wrapper ****** 
    # used to avoid errors of operation on fields like (multiply decimal with float)
    discount_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    queryset = Product.objects.annotate(
        discount_price=discount_price
    )


    #      ******** Quering Generic Relationships ****** look at tags/models.tagItem




#****************
#    stop at 3.20 m (nearly)
#****************
    # return HttpResponse('hello from django')
    return render(req, 'hello.html' , {'name': 'ahmed' , 'age': 20, 'result': list(queryset)})

