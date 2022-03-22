from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .models import *
from store.models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.urls import reverse
#ssl commerz intregation
from django.conf import settings
import json
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.
class CheckOutView(View):
    def get(self, request, *args, **kwargs):
        try:
            form = BillingAddressForm()
            payment_method = PaymentMethodForm()
            order = Order.objects.get(user=request.user, ordered=False)


            context = {
                'form': form,
                'payment_method': payment_method,
                'order':order,
            }
            return render(request, 'checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(request, 'You have no active order')
            return redirect('/')

    def post(self, request, *args, **kwargs):
        form = BillingAddressForm(request.POST)
        payment_obj = Order.objects.filter(user=request.user, ordered=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        
        if request.method == 'post' or request.method == 'POST':
            form = BillingAddressForm(request.POST)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():

                first_name =form.cleaned_data.get('first_name')
                last_name =form.cleaned_data.get('last_name')
                company_name =form.cleaned_data.get('company_name')
                street_address =form.cleaned_data.get('street_address')
                apartment_address =form.cleaned_data.get('apartment_address')
                country =form.cleaned_data.get('country')
                city =form.cleaned_data.get('city')
                state =form.cleaned_data.get('state')
                zip =form.cleaned_data.get('zip')
                phone =form.cleaned_data.get('phone')
                email =form.cleaned_data.get('email')
                order_note =form.cleaned_data.get('order_note')

                billing_address  = BillingAddress(
                    user=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    company_name=company_name,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    city=city,
                    state=state,
                    zip=zip,
                    phone=phone,
                    email=email,
                    order_note=order_note
                )
                billing_address.save()
                payment_obj.billing_address =billing_address
                pay_method = pay_form.save()

                if pay_method.payment_option == 'Cash On Delivery':
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order = order_qs[0]
                    order.ordered = True
                    order.orderId = order.id
                    order.paymentId = pay_method.payment_option
                    

                    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
                    for order_item in order_items:
                        order_item.ordered = True
                        order_item.save()

                    order.save()
                    messages.success(request, "You order was successful")
                    return redirect('/')

                elif pay_method.payment_option == 'SSL Commerce':
                    store_id = settings.STORE_ID
                    store_pass = settings.STORE_PASS
                    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)
                    
                    status_url = request.build_absolute_uri(reverse('status'))
                    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order_items = order_qs[0].items.all()
                    order_item_count = order_qs[0].items.count()
                    order_total = order_qs[0].total()
                    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='clothing', product_name=order_items, num_of_item=order_item_count, shipping_method='YES', product_profile='None')
                
                    current_user = request.user
                    mypayment.set_customer_info(name=current_user.username, email=current_user.email, address1='demo1', address2='demo2', city='Dhaka', postcode=1207, country='Bangladesh', phone='01704870490')
                    
                    # billing_address = BillingAddress.objects.filter(user=request.user)[0]
                    mypayment.set_shipping_info(shipping_to=current_user.username, address='demo3', city='Dhaka', postcode=1207, country='Bangladesh')
                    
                    response_data = mypayment.init_payment()
                    
                    return redirect(response_data['GatewayPageURL'])
                return redirect('Check-Out')

@csrf_exempt
def sslc_status(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']

            return HttpResponseRedirect(reverse('sslc-complete', kwargs={'val_id': val_id, 'tran_id': tran_id}))
    return render(request, 'status.html')

def sslc_complete(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.orderId = val_id
    order.paymentId = tran_id
    order.save()
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
    for item in cart_items:
        item.ordered = True
        item.save()
    messages.success(request, "You order was successful")
    return redirect('/')