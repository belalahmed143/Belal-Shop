from django.db import models
import string, random
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from paymentApp.models import BillingAddress
# Create your models here.

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    img = models.ImageField(upload_to='CategoryImg')

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='brandImg')
    def __str__(self):
        return self.name

class Banner(models.Model):
    BANNER_TYPE =(
        ("Caro" , "Caro"),
        ("first_p_add" , "first_p_add"),
        ("second_p_add" , "second_p_add"),
    )
    banner_type =models.CharField(max_length=100,choices=BANNER_TYPE, default='Caro')
    cate = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True,null=True)   
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=50)
    image =models.ImageField(upload_to='bannerImg')

    def __str__(self):
        return self.title

class Product (models.Model):
    product_name = models.CharField(max_length=60)
    slug = models.SlugField(max_length = 50,blank=True, null=True)  
    categoris = models.ForeignKey(ProductCategory, verbose_name='Product Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ProductImg',default='ProductImg/noimg.jpg')
    hover_image = models.ImageField(upload_to='ProductImg',default='noimg.jpg', blank=True, null=True)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    product_color = models.CharField(max_length = 150,blank=True, null=True)
    size = models.CharField(max_length = 150,blank=True, null=True)
    sort_discription = models.TextField()
    discription = RichTextField()
    aditional_discription = models.TextField(blank=True, null=True)
    in_stock = models.BooleanField(default=True)

    SALE_TYPE =(
        ('Feature', 'Feature'),
        ('OneSale', 'OneSale'),
        ('TopRate', 'TopRate')
    )
    sale_type = models.CharField(max_length=50, choices=SALE_TYPE, blank=True, null=True)
    
    LABEL =(
        ('New', 'New'),
        ('Offer', 'Offer'),
        ('Out', 'Out')
    )
    label = models.CharField(max_length=50, choices=LABEL, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    
    def saving_price(self):
        return self.price  - self.discount_price

    def saving_percent(self):
        return self.saving_price() / self.price  * 100
        
    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-id']
    
    def save(self, *args, **kwargs):
        try:
            self.slug = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(49))
            super().save(*args, **kwargs)
        except IntegrityError:
            self.save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})
    
    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})

class ProductImgGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to='ProductImgGallery')

    def __str__(self):
        return self.product.slug

class VariationManager(models.Manager): 
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')


VAR_CATEGORIES = ( 
    ('size', 'size'), 
    ('color', 'color'), 
    ('package', 'package'), )

class Variation(models.Model): 
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES) 
    title = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    objects = VariationManager()

    def __str__(self):
        return self.title

class OrderItem(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    ordered = models.BooleanField(default=False) 
    item = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.IntegerField(default=1) 
    variation = models.ManyToManyField(Variation)

    def saving_price(self):
        return self.item.price * self.quantity - self.item.discount_price * self.quantity

    def saving_percent(self):
        return (self.saving_price()) / (self.item.price * self.quantity) * 100

    def get_subtotal(self):
        if self.item.discount_price:
            return self.item.discount_price * self.quantity
        else:
            return self.item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.item.product_name}"


class Order(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    items = models.ManyToManyField(OrderItem) 
    start_date = models.DateTimeField(auto_now_add=True) 
    ordered_date = models.DateTimeField() 
    ordered = models.BooleanField(default=False)
    orderId = models.CharField(max_length = 150, blank=True, null=True)
    paymentId = models.CharField(max_length = 150, blank=True, null=True) 
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, blank=True, null=True)
    payment_option = models.CharField(max_length = 150)
    shiping_charge = models.IntegerField(default=60)
    
    
    def __str__(self):
        return self.user.username   

    def get_total(self):
        total = 0
        for i in self.items.all():
            total += i.get_subtotal()
        return total

    def get_total_with_shiping_charge(self):
        total = 0
        for i in self.items.all():
            total += i.get_subtotal()
        total += self.shiping_charge
        return total

    def get_total_with_coupon(self):
        total = 0 
        for i in self.items.all():
            total += i.get_subtotal()
        total += self.shiping_charge
        total -= self.coupon.amount
        return total

    def total(self):
        if self.coupon:
            return self.get_total_with_coupon()
        else:
            return self.get_total_with_shiping_charge()

class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    valid_from = models.DateTimeField(null=True)
    valid_to = models.DateTimeField(null=True)
    max_value = models.IntegerField(validators=[MaxValueValidator(100)], verbose_name='Coupon Quantity', null=True) # No. of coupon
    used = models.IntegerField(default=0)
    
    def __str__(self):
        return self.code
    
#WishListMOdel

class WhishLIst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wish_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.CharField(max_length=30,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.wish_product.product_name
    
    
    
    
    
    
    

    
    