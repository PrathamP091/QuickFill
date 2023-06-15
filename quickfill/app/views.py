from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.views import View
from . models import Product, Customer, Cart, Payment, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
def index(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/index.html', locals())

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/about.html', locals())

def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/contact.html', locals())

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        name = Product.objects.filter(category=val).values('name')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/category.html', locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(name=val)
        name = Product.objects.filter(category=product[0].category).values('name')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/category.html', locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congatulations! User has been Registered Successfully")
            return render(request, '/accounts/login', locals())
        else:
            messages.warning(request, "Invalid Input")
            return render(request, 'app/customerregistration.html', locals())
        
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            mobile = form.cleaned_data['mobile']

            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode, mobile=mobile)
            reg.save()
            messages.success(request, "Congatulations! Profile saved Successfully")
        else:
            messages.warning(request, "Invalid Input")
        return render(request, 'app/profile.html', locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.mobile = form.cleaned_data['mobile']
            add.save()
            messages.success(request, "Congatulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input")
        return redirect("address")
    
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.price
        amount = amount + value
    totalamount = amount + 0
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 0
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 0
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product_id=prod_id)& Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 0
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.price
            famount = famount + value
        totalamount = famount + 0
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12" }
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_M2ARinm7fzBT7C', 'entity': 'order', 'amount': 279000, 'amount_paid': 0, 'amount_due': 279000, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1686823775}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html', locals())
    
@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')

    user = request.user
    #return redirect("orders")
    customer = Customer.objects.get(id = cust_id)
    #to update payment status and payment id
    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #to save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())