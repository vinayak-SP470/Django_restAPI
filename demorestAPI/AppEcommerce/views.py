from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, ProductForm
from .models import Product


# Home page view
# def homePage(request):
#     return render(request, template_name="home.html")

# User signup logic
def user_signup(request):
    if request.method == 'POST':
        print(request.POST)
        user_reg_form = UserRegistrationForm(request.POST)
        # print("-----user_reg_form.errors-----", user_reg_form.errors)
        if user_reg_form.is_valid():
            new_user = user_reg_form.save(commit=False)
            # new_user.set_password(user_reg_form.cleaned_data['password1'])
            new_user.save()
            return render(request,'home.html',{'user_reg_form':user_reg_form})
    else:
        user_reg_form = UserRegistrationForm()
    return render(request,'signup.html',{'user_reg_form':user_reg_form})

# user login logic
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

# user logout logic
def logout_user(request):
    logout(request)
    return redirect('home')

# Custom error message for invalid username or password
class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Please enter a correct username and password. Both fields may be case-sensitive.",
    }

def seller_products(request):
    if request.user.is_authenticated and request.user.role.name == 'Seller':
        searchterm = request.GET.get('searchproduct')
        sort_by = request.GET.get('sort_by', 'price')  # Default sorting by price
        ascending = request.GET.get('ascending', 'true').lower() == 'true'  # Default ascending order

        if searchterm:
            searched_products = Product.objects.filter(productname__icontains=searchterm)
        else:
            searched_products = Product.objects.filter(seller=request.user)
        if sort_by == 'price':
            searched_products = searched_products.order_by('price' if ascending else '-price')
        return render(request, 'home.html', {'searched_products': searched_products, 'searchterm': searchterm})
    else:
        return render(request, 'home.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('home')
