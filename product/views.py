from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from accounts.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views import View
import random
#  Create your views here. 

# To render the landing page of the project
class home(View):
    template_name = 'index.html'
    
    def get_context_data(self):
        prods = MenClothing.objects.filter(is_featured=True)
        bannerimage = BannerImage.objects.all()
        cartitem = Cart.objects.filter(user=self.request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        context = {
            'prods': prods,
            'bannerimage': bannerimage,
            'cartitem': cartitem,
            'total_quantity': total_quantity,
        }

        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context) 

# To get product details of each product
class productdetail(View):
    template_name = 'product-detail.html'
    
    def get_context_data(self, product_id):
        product = get_object_or_404(MenClothing, pk=product_id)
        cartitem = Cart.objects.filter(user=self.request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        context = {
            'product': product,
            'cartitem': cartitem,
            'total_quantity': total_quantity,
        }

        return context

    def get(self, request, product_id):
        context = self.get_context_data(product_id)
        return render(request, self.template_name, context)

# # To get tshirt category
# class tshirt_category(View):
#     template_name = 'category.html'
    
#     def get_context_data(self):
#         tshirts = MenClothing.objects.filter(category__name='T-shirt', is_featured=True)
#         cartitem = Cart.objects.filter(user=self.request.user.id)
#         total_quantity = sum(item.product_qty for item in cartitem)
#         context = {
#             'category': 'T-shirt',
#             'products': tshirts,
#             'total_quantity': total_quantity,
#         }

#         return context

#     def get(self, request):
#         context = self.get_context_data()
#         return render(request, self.template_name, context)

# # To get shirt category
# class shirt_category(View):
#     template_name = 'category.html'
    
#     def get_context_data(self):       
#         shirts = MenClothing.objects.filter(category__name='Shirt', is_featured=True)
#         cartitem = Cart.objects.filter(user=self.request.user.id)
#         total_quantity = sum(item.product_qty for item in cartitem)
#         context = {
#             'category': 'Shirt',
#             'products': shirts,
#             'total_quantity': total_quantity,
#         }

#         return context

#     def get(self, request):
#         context = self.get_context_data()
#         return render(request, self.template_name, context)

# # To get jeans category
# class jeans_category(View):
#     template_name = 'category.html'
    
#     def get_context_data(self):
#         jeans = MenClothing.objects.filter(category__name='Jeans', is_featured=True)
#         cartitem = Cart.objects.filter(user=self.request.user.id)
#         total_quantity = sum(item.product_qty for item in cartitem)
#         context = {
#             'category': 'Jeans',
#             'products': jeans,
#             'total_quantity': total_quantity,
#         }

#         return context

#     def get(self, request):
#         context = self.get_context_data()
#         return render(request, self.template_name, context)

# # To get jacket category
# class jacket_category(View):
#     template_name = 'category.html'
    
#     def get_context_data(self):
#         jackets = MenClothing.objects.filter(category__name='Jacket', is_featured=True)
#         cartitem = Cart.objects.filter(user=self.request.user.id)
#         total_quantity = sum(item.product_qty for item in cartitem)
#         context = {
#             'category': 'Jacket',
#             'products': jackets,
#             'total_quantity': total_quantity,
#         }

#         return context

#     def get(self, request):
#         context = self.get_context_data()
#         return render(request, self.template_name, context)

# To get the category page separatly
class CategoryView(View):
    template_name = 'category.html'

    def get_context_data(self, category_name):
        predefined_categories = ['T-shirt','Shirt','Jacket','Jeans']
        if category_name:
            category_items = MenClothing.objects.filter(category__name__iexact=category_name, is_featured=True)
        else:
            category_items = MenClothing.objects.filter(category__name__iexact__in=predefined_categories, is_featured=True)

        cart_items = Cart.objects.filter(user=self.request.user.id)
        total_quantity = sum(item.product_qty for item in cart_items)

        context = {
            'categories': predefined_categories,
            'category_name': category_name,
            'products': category_items,
            'total_quantity': total_quantity,
        }

        return context

    def get(self, request, category_name=None):
        context = self.get_context_data(category_name)
        return render(request, self.template_name, context)
 
# To add product to the cart
class addtocart(View):
    def post(self, request):
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = MenClothing.objects.get(id=prod_id)

            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=prod_id).exists():
                    return JsonResponse({'status': 'Product Already in Cart'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': 'Product added successfully'})
                    else:
                        return JsonResponse({'status': f'Only {product_check.quantity} quantity available'})
            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': 'Login to Continue'})

    def get(self, request):
        return redirect('index')

# cart page
class cart(View):
    def get(self, request):
        if request.user.is_authenticated:
            cartitem = Cart.objects.filter(user=request.user.id).order_by('-created_at')
            total_quantity = sum(item.product_qty for item in cartitem)
            total_price = sum(item.product.price * item.product_qty for item in cartitem)

            context = {'cartitem': cartitem, 'total_quantity': total_quantity, 'total_price': total_price}
            return render(request, 'cart.html', context)
        else:
             return redirect('loginpage')
         
# To update the product quantity in the cart
class updatecart(View):
    def post(self, request):
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user.id, product_id=prod_id).exists():
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user.id)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': 'Updated Successfully'})
        return redirect('index')

# To delete the product added in the cart
class deletecartitem(View):
    def post(self, request):
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
            return JsonResponse({'status': 'Deleted Successfully'})
        return redirect('index')

# Wishlist page
class wishlist(View):
    def get(self, request):
        if request.user.is_authenticated:
            cartitem = Cart.objects.filter(user=request.user.id)
            total_quantity = sum(item.product_qty for item in cartitem)
            wishlist = Wishlist.objects.filter(user=request.user.id)
            context = {'wishlist': wishlist, 'total_quantity': total_quantity}
            return render(request, 'wishlist.html', context)
        else:
            return redirect('loginpage')

# To add product to the wishlist
class addtowishlist(View):
    def post(self, request):
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = MenClothing.objects.get(id=prod_id)
            if product_check:
                if Wishlist.objects.filter(user=request.user, product_id=prod_id):
                    return JsonResponse({'status': 'Product already in wishlist'})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': 'Product added to wishlist'})
            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': 'Login to continue'})
        
   
        

# To delete product from the wishlist
class deletewishlistitem(View):
    def post(self, request):
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if Wishlist.objects.filter(user=request.user, product_id=prod_id).exists():
                wishlistitem = Wishlist.objects.get(user=request.user, product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status': 'Product removed from wishlist'})
            else:
                return JsonResponse({'status': 'Product not found in wishlist'})
        else:
            return JsonResponse({'status': 'Login to continue'})
        
    def get(self, request):
        return redirect('index')

# checkout page
class checkoutpage(View):
    def get(self, request):
        rawcart = Cart.objects.filter(user=request.user)
        total_quantity = sum(item.product_qty for item in rawcart)
        
        for item in rawcart:
            if item.product_qty > item.product.quantity:
                item.delete()

        cartitems = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.product_qty for item in cartitems)
        
        userprofile = Profile.objects.filter(user=request.user).first()

        context = {'cartitems': cartitems, 'total_price': total_price, 'total_quantity': total_quantity, 'userprofile': userprofile}
        return render(request, 'place-order.html', context)


# To placeorder a product
class placeorder(View):
    def post(self, request):
        currentuser = User.objects.filter(id=request.user.id).first()
        
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('firstname')
            currentuser.last_name = request.POST.get('lastname')
            currentuser.save()
            
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()
            
        neworder = Order()
        neworder.user = request.user
        neworder.firstname = request.POST.get('firstname')
        neworder.lastname = request.POST.get('lastname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = sum(item.product.price * item.product_qty for item in cart)
        
        neworder.total_price = cart_total_price
        trackno = 'Hello' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'Hello' + str(random.randint(1111111, 9999999))
            
        neworder.tracking_no = trackno
        neworder.save()
        
        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.product_qty
            )
            
            orderproduct = MenClothing.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()
        
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Your Order has be placed successfully")
        return redirect('index')
  
    
# To see all products using pagination
class store(View):
    def get(self, request):
        prods = MenClothing.objects.filter(is_featured=True).order_by('image')
        cartitem = Cart.objects.filter(user=request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        category = Category.objects.all()
        paginator = Paginator(prods, 3)
        page = request.GET.get('page')
        
        try:
            prods = paginator.page(page)
        except PageNotAnInteger:
            prods = paginator.page(1)
        except EmptyPage:
            prods = paginator.page(paginator.num_pages)
        
        context = {'prods': prods, 'page': page, 'category': category, 'total_quantity': total_quantity}
        return render(request, 'store.html', context)
  
class productlist(View):
    def get(self, request, *args, **kwargs):
        products = MenClothing.objects.filter(is_featured=True).values_list('name', flat=True)
        productList = list(products)
        return JsonResponse(productList, safe=False)
    
    
class searchproduct(View):
    def post(self, request, *args, **kwargs):
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = MenClothing.objects.filter(name__contains=searchedterm).first()
            if product:
                return redirect('category/')
        