from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    city = models.CharField(max_length = 150)
    state = models.CharField(max_length = 150) 
    zip =models.CharField(max_length=100)
    phone =models.CharField(max_length=11)
    email = models.EmailField()
    order_note = models.TextField()     
    
    def __str__(self):
        return self.user.username
        
    # def is_fully_filled(self):
    #     field_names = [f.name for f in self._meta.get_fields()]
    #     for field_name in field_names:
    #         value = getattr(self, field_name)
    #         if value is None or value == '':
    #             return False
    #     return True

    class Meta:
        verbose_name_plural='BillingAddress'