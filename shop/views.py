from django.shortcuts import render , HttpResponse ,redirect , get_object_or_404
from .models import *
from accounts.models import SellerProfile , CustomUser , UserProfile , address
from .forms import ProductForm , CategoryForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required 
from django.db import transaction
# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request , 'shop/products.html' , context)

def dashboard(request):
        if request.user.is_seller:
            user = SellerProfile.objects.get(user = request.user)
            total_products = Product.objects.filter(seller = user).count()
            total_orders  = OrderItem.objects.filter(seller = user).count()
            total_revenue = OrderItem.objects.filter(seller = user).annotate(total_price = models.F('price') * models.F('quantity')).aggregate(total_revenue = models.Sum('total_price'))['total_revenue']
            total_customers = OrderItem.objects.filter(seller = user).values('user').distinct().count()
            context = {'user': user , 'total_products':total_products , 'total_orders':total_orders , 'total_revenue':total_revenue , 'total_customers':total_customers}
            return render(request, 'shop/seller/dashboard.html' ,context)
        elif request.user.is_superuser:
            products = Product.objects.all()
            total_products = Product.objects.all().count()
            total_orders  = OrderItem.objects.all().count()
            total_revenue = OrderItem.objects.all().annotate(total_price = models.F('price') * models.F('quantity')).aggregate(total_revenue = models.Sum('total_price'))['total_revenue']
            total_customers = OrderItem.objects.values('user').distinct().count()
            context = {'products': products , 'total_products':total_products , 'total_orders':total_orders , 'total_revenue':total_revenue , 'total_customers':total_customers}
            return render(request, 'shop/seller/dashboard.html' ,context)
        else:
            return HttpResponse("You are not authorized to view this page")

class SellerAction:
    def add_category(request):
        if request.user.is_seller:
            if request.method == 'POST':
                category = Category.objects.create(name=request.POST['name'])
                return redirect('/shop/add_category/')
            form = CategoryForm()
            context = {'form': form}
            return render(request, 'shop/add_categories.html' , context)
        else:
            return HttpResponse("You are not authorized to add category")
    def create_product(request):
        user = SellerProfile.objects.get(user=request.user)
        if request.user.is_seller:
            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.seller = user
                    product.save()
                    form.save_m2m()  # Save many-to-many relationships
                    return redirect('/shop/manage_products/')
            else:
                form = ProductForm()
            return render(request, 'shop/seller/create_product.html', {'form': form})
                
    def manage_product(request):
        if request.user.is_seller:
            user = SellerProfile.objects.get(user = request.user)
            
            products = Product.objects.filter(seller = user)
            context = {'products': products}
            return render(request, 'shop/seller/manage_products.html' ,context)
        elif request.user.is_superuser:
            products = Product.objects.all()
            context = {'products': products}
            return render(request, 'shop/seller/manage_products.html' ,context)

        else:
            return HttpResponse("You are not authorized to manage products")

    
    def edit_product(request, id):
        product = get_object_or_404(Product, id=id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request , "Product was successfully updated")
                return redirect('/shop/manage_products/')  
        else:
            form = ProductForm(instance=product)
        return render(request, 'shop/seller/create_product.html', {'form': form, 'product': product})

        
    def view_product(request, id):
        product = get_object_or_404(Product, id=id)
        return render(request, 'shop/view_product.html', {'product': product})
    
    def delete_product(request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()   
        messages.success(request , "Product successfully deleted")
        return redirect('/shop/manage_products/')
        
class CartAction:
    
    @login_required
    def add_to_cart(request, id):
        if request.method == 'POST':
            product = Product.objects.get(pk=id)
            color = request.POST.get('color')
            size = request.POST.get('size')
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product , seller = product.seller , color = color , size = size)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return redirect('/shop/cart/')
        else:
            return redirect('/shop/')
    @login_required
    def update_quantity(request, id):
        cart_item = get_object_or_404(Cart, id=id)

        if request.method == 'POST':
            new_quantity = int(request.POST.get('quantity', 0))
            if new_quantity >= 0:
                cart_item.quantity = new_quantity
                cart_item.save()
                return redirect('cart')

        return redirect('cart')
    
    
    
    @login_required
    def remove_from_cart(request, id):
        cart_item = Cart.objects.get(pk=id)
        cart_item.delete()
        return redirect('cart')
    @login_required
    def cart(request):
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        if cart_items:
            return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})
        else:
            messages.error(request,'add something in cart')
            return redirect('/')
    @login_required
    @transaction.atomic
    def checkout(request):  
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        if request.method == 'POST':
            user = request.user
            addr = request.POST['address']
            order = Order.objects.create(user=request.user, total_amount=total_price)
            for cart_item in cart_items:
                OrderItem.objects.create(product=cart_item.product, quantity=cart_item.quantity, price=cart_item.product.price , address=addr, order=order , user=user , seller = cart_item.seller)
            cart_items.delete()
            return render(request, 'shop/order_placed.html')
        else:
            addresses  = address.objects.filter(user = request.user)
            return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total_price': total_price,'addresses':addresses})

   
    def order_detail(request , id):
        order = OrderItem.objects.get(id = id)
        return render(request, 'shop/order_details.html', {'order': order})


def search_products(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    
    if category_id:
        products = products.filter(category=category_id)
    
    return render(request, 'shop/products.html', {'products': products})

@login_required
def orders(request):
    if request.user.is_superuser :
        orders = OrderItem.objects.all()
        context = {'orders':orders}
        return render(request , 'shop/order_history.html', context)
    elif request.user.is_seller:
        user = SellerProfile.objects.get(user = request.user)
        orders = OrderItem.objects.filter(seller = user)
        if request.method == 'POST':
            order_id = request.POST['order_id']
            order = OrderItem.objects.get(id = order_id)
            order.status = request.POST['status']
            order.save()
            return redirect('/shop/orders/')
        context = {'orders':orders}
        return render(request , 'shop/order_history.html', context)
    else:
        order = OrderItem.objects.filter(user = request.user)
        context = {'orders':order}
        return render(request , 'shop/order_history.html', context)
    