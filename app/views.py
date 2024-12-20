from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Customer, OrderPlaced, Product, Cart, WishList
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#from django.db.models import Count

@login_required
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())

@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())

@method_decorator(login_required, name="dispatch")
class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())

@method_decorator(login_required, name="dispatch")
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))
        return render(request, "app/category.html", locals())

@method_decorator(login_required, name="dispatch")   
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = WishList.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))
        return render(request, "app/product_detail.html", locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Congratuliosn! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        
        return render(request, "app/customerregistration.html", locals())

@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'app/profile.html', locals())

@login_required 
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/address.html", locals())

@method_decorator(login_required, name="dispatch")
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))
        return render(request, "app/updateAddress.html", locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")

@login_required  
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/addtocart.html", locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    product = WishList.objects.filter(user=request.user)
    return render(request, "app/wishlist.html", locals())

@method_decorator(login_required, name="dispatch")
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, "app/checkout.html", locals())

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, "app/orders.html", locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id') 
        try:
            c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
            if c:
                c.quantity += 1 
                c.save()  
            else:
                return JsonResponse({'error': 'Cart item not found.'}, status=404)

            cart = Cart.objects.filter(user=request.user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount += value
            totalamount = amount + 40 

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id') 
        try:
            c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
            if c:
                c.quantity -= 1 
                c.save()  
            else:
                return JsonResponse({'error': 'Cart item not found.'}, status=404)

            cart = Cart.objects.filter(user=request.user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount += value
            totalamount = amount + 40 

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
            if c.exists():
                c.delete()  
            else:
                return JsonResponse({'error': 'Cart item not found.'}, status=404)

            cart = Cart.objects.filter(user=request.user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount += value
            totalamount = amount + 40  

            data = {
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
def plus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')  
        try:
            product = get_object_or_404(Product, id=prod_id)
            user = request.user

            if WishList.objects.filter(user=user, product=product).exists():
                data = {'message': 'Product is already in your WishList'}
            else:
                WishList(user=user, product=product).save()
                data = {'message': 'WishList Added Successfully'}

            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        try:
            product = get_object_or_404(Product, id=prod_id)
            user = request.user

            wishlist_item = WishList.objects.filter(user=user, product=product)
            if wishlist_item.exists():
                wishlist_item.delete()
                data = {'message': 'WishList Removed Successfully'}
            else:
                data = {'message': 'Product is not in your WishList'}

            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required      
def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query))
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/search.html", locals())