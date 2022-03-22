from django.contrib import admin
from .models import *
# Register your models here.
class ProductImgGalleryAdmin(admin.StackedInline):
    model = ProductImgGallery
    min_num = 3
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImgGalleryAdmin]

admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Variation)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(WhishLIst)