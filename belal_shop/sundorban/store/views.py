from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View,DetailView
from .models import *
from .forms import *
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductView(View):
    def get(self,request):
        products = Product.objects.all().order_by('?')
        lighting = Product.objects.filter(categoris__category_name='Lighting')
        decoration = Product.objects.filter(categoris__category_name='Decoration')
        furniture = Product.objects.filter(categoris__category_name='Furniture')
        banner = Banner.objects.all()
        brand = Brand.objects.all()
        
        context={
            'products': products,
            'banner':banner,
            'brand' :brand,
            'lighting':lighting,
            'decoration':decoration,
            'furniture':furniture
        }    
        return render(request, 'index.html',context)
        
    def post(self, request):
        pass


class ProductDetail(DetailView):
    model = Product
    template_name = "product_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        img = ProductImgGallery.objects.filter(product=self.object.id)
        
        slug =self.kwargs['slug']
        prod = Product.objects.get(slug=slug)
        related_product = Product.objects.filter(categoris=prod.categoris).exclude(slug=slug)
        # print(related_product)

        context['img'] = img
        context['related_product'] = related_product
        return context

class ProductSearchView(View):

    def get(self,request):
        query = request.GET['q']
        search_item = Q(product_name__icontains=query) | Q(price__icontains=query) | Q(categoris__category_name__icontains=query)
        products = Product.objects.filter(search_item)

        context ={
            'products' : products
        }

        return render(request, 'search_product.html', context)     

class ProductCategoryFiltering(View):
    def get(self,request,name):
        cate = get_object_or_404(ProductCategory,category_name=name)
        products = Product.objects.filter(categoris=cate.id)

        context ={
            'products':products
        }
        return render(request, 'category.html', context )
    
    def post(self, request):
        pass

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Product,slug=slug) 
    order_item_qs = OrderItem.objects.filter( item=item, user=request.user, ordered=False)
    
    item_var = [] #item variation
    if request.method == 'POST':
        for items in request.POST:
            key = items
            val = request.POST[key]
            try:
                v = Variation.objects.get(
                    item=item,
                    category__iexact=key,
                    title__iexact=val
                )
                item_var.append(v)
            except:
                pass

        if len(item_var) > 0:
                #order_item_qs.variation.clear()
                for items in item_var:
                    order_item_qs = order_item_qs.filter(
                        variation__exact=items,
                    )
    if order_item_qs.exists():
        order_item = order_item_qs[0]
        # for order_item in order_item_qs:
        # order_item = order_item_qs.first()
        quantity = request.POST.get('quantity')
        if quantity:
            order_item.quantity += int(quantity)
        else:
            order_item.quantity = int(quantity)
        order_item.save()
        #print(order_item_qs)

    else:
        order_item = OrderItem.objects.create(
            item=item,
            user=request.user,
            ordered=False
        )
        quantity = request.POST.get('quantity')
        order_item.quantity = int(quantity)
        order_item.variation.add(*item_var)
        order_item.save()

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if not order.items.filter(item__id=order_item.id).exists():
            order.items.add(order_item)
            messages.success(request, "Thank You successfully add")
            return redirect('product-detail', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to cart.")
        return redirect('product-detail', slug=slug)


class CartSummary(View,LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        try:
            order =Order.objects.get(user=request.user, ordered=False)
            form = CouponCodeForm(request.POST or None)
            context={
                'order':order,
                'form':form,
            }
            return render(request, 'cart_summary.html', context)
        
        except ObjectDoesNotExist:
            return redirect('/')



class AddCouponView(View,LoginRequiredMixin):
    def post(self, *args, **kwargs):
        now = timezone.now()
        form = CouponCodeForm(self.request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            order = Order.objects.get(user=self.request.user, ordered=False)
            coupon = Coupon.objects.filter(code__iexact=code, valid_from__lte=now, valid_to__gte=now).exclude(order__user=self.request.user,max_value__lte=F('used')).first()
            if not coupon:
                messages.error(self.request, 'You can\'t use same coupon again, or coupon does not exist')
                return redirect('cart-summary')
            else:
                try:
                    coupon.used += 1
                    coupon.save()
                    order.coupon = coupon
                    order.save()
                    messages.success(self.request, "Successfully added coupon")
                except:
                    messages.error(self.request, "Max level exceeded for coupon")
                
                return redirect('cart-summary')


class PrductQuantityIncrement(View,LoginRequiredMixin):
    def get(self,request, *args, **kwargs):
        slug = self.kwargs['slug']
        item = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, "This product quantity was update")
                    return redirect("cart-summary")
            else:
                messages.info(request, "This item was not in your cart")
                return redirect("cart-summary", slug=slug)
        else:
            messages.info(request, "You do not have an active order")
            return redirect("cart-summary", slug=slug)



class PrductQuantityDecrementr(View,LoginRequiredMixin):
    def get(self,request, *args, **kwargs):
        slug = self.kwargs['slug']
        item = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, "This product quantity was update")
                    return redirect("cart-summary")
                else:
                    order_item.delete()
                    messages.info(request, "This product delete from cart")
                return redirect("cart-summary")
            else:
                messages.info(request, "This item was not in your cart")
                return redirect("cart-summary", slug=slug)
        else:
            messages.info(request, "You do not have an active order")
            return redirect("cart-summary", slug=slug)

#WishList


@login_required
def add_to_wishlist(request,slug):
    products = get_object_or_404(Product, slug=slug)
    wish_product, created = WhishLIst.objects.get_or_create(wish_product=products, slug=products.slug, user=request.user)
    messages.info(request, "This Product add your wish list")
    return redirect('home')

def wish_list(request):
    wish_product = WhishLIst.objects.filter(user=request.user)

    context={
        'wish_product': wish_product
    }
    return render(request, 'wishlist.html', context)

def delete_wish_list(request, slug):
    wish_product = WhishLIst.objects.filter(user=request.user, slug=slug)
    wish_product.delete()
    messages.info(request, "this product delete from your wish list")
    return redirect('wish-list')




