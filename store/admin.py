from django.contrib import admin, messages
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html , urlencode
from django.urls import reverse
# from django.contrib.contenttypes.admin import GenericTabularInline
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    def lookups(self, request, model_admin):
        return [
            ('<10' , 'low')
        ]
    def queryset(self, request, queryset):
        if self.value() == '<10': #this return the selected filter
            return queryset.filter(inventory__lt=10)
        


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title', 'slug'] #fields you want to show when trying to add product using the admin panel 
    # exclude = ['title', 'slug'] # the opposit
    # readonly_fields = ['title'] # make field read only
    prepopulated_fields = {
        'slug': ['title'] # could be ['title', .....] many fields
    }
    autocomplete_fields = ['collection']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update' , InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['title']
    # inlines = [TagInline]
    # for all options search django modelAdmin 
    
    @admin.display(ordering='inventory')
    def inventory_status(self, Product):
        if Product.inventory < 10:
            return 'LOW'
        else:
            return 'OK'
    
    # without select_related this make individual query for each call
    def collection_title(self, product):
        return product.collection.title

    @admin.action(description='clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were updated',
            messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'customer_orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    # search_fields =['first_name', 'last_name'] # in this shape it would search for any 'word' that contain the char , but we could use any look up type like startswith
    search_fields =['first_name__istartswith', 'last_name__istartswith']


    @admin.display(ordering='customer_orders')
    def customer_orders(self , customer):
        url=(
            reverse('admin:store_customer_changelist')
            + '?'
            + urlencode({
                'customer__id':str(customer.id)
            })
        )
        return f'{customer.customer_orders} Orders'
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            customer_orders=Count('order')
        )


# ovveride the base query set

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields= ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # reverse('admin:app_model_page')
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
            )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        # return collection.products_count #no field with this name 
    #this is where we need to override the queryset of this page and annotate our collections with the number of their products
    #so use get_queryset method
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
    


# admin.site.register(models.Product, ProductAdmin) >> changed with the decorator up there

# we use TabularInline or StackedInline   >: difference is that StackedInline put them stacked under each other 
class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','payment_status', 'customer_name']
    list_select_related = ['customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

    def customer_name(self, order):
        return f'{order.customer.first_name} {order.customer.last_name}'
