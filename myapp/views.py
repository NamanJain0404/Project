from django.shortcuts import render,HttpResponse , redirect
from django.contrib import messages
from .models import *
from django.core.mail import send_mail
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password
# from .models import OTPModel
# Create your views here.
from django.core.paginator import Paginator

def msg(request):
    return HttpResponse("hello python django")

def blog_details(request):
    cid=category.objects.all().order_by("-id")
    uid=user.objects.get(username=request.session['username'])
    wid_count=wishlist.objects.filter(user=uid).count()
    cid_count=cart.objects.filter(user=uid).count()
    contaxt={
            "cid":cid,
            "uid":uid,
            "wid_count": wid_count,
            "cid_count": cid_count,
        }
    return render(request,"blog_details.html", contaxt)

def blog(request):
    cid=category.objects.all().order_by("-id")
    pid=product.objects.all().order_by("-id")
    uid=user.objects.get(username=request.session['username'])
    wid_count=wishlist.objects.filter(user=uid).count()
    cid_count=cart.objects.filter(user=uid).count()
    pagination=Paginator(pid,1)
    page=request.GET.get("page")
    pid=pagination.get_page(page)
    contaxt={
            "cid":cid,
            "pid":pid,
            "uid":uid,
            "wid_count": wid_count,
            "cid_count": cid_count,
        }
    return render(request,"blog.html", contaxt)

def checkout(request):
        cid=category.objects.all().order_by("-id")
        uid=user.objects.get(username=request.session['username'])
        wid_count=wishlist.objects.filter(user=uid).count()
        cid_count=cart.objects.filter(user=uid).count()
        cart_items = cart.objects.filter(user=uid).select_related('product')

        subtotal=sum(item.total_price for item in cart_items)
        shipping=0 if subtotal>99 else 20
        total=subtotal+shipping

        contaxt={
                "cid":cid,
                "uid":uid,
                "wid_count": wid_count,
                "cid_count": cid_count,
                "cart_items":cart_items,
                "subtotal":subtotal,
                "shipping":shipping,
                "total":total,
            }
        return render(request,"checkout.html", contaxt)

def contact(request):
    cid=category.objects.all().order_by("-id")
    uid=user.objects.get(username=request.session['username'])
    wid_count=wishlist.objects.filter(user=uid).count()
    cid_count=cart.objects.filter(user=uid).count()
    contaxt={
            "cid":cid,
            "uid":uid,
            "wid_count": wid_count,
            "cid_count": cid_count,
        }
    return render(request,"contact.html", contaxt)

def index(request):
    if "username" in request.session:
        cid=category.objects.all().order_by("-id")
        pid=product.objects.all().order_by("-id")
        uid=user.objects.get(username=request.session['username'])
        wid_count=wishlist.objects.filter(user=uid).count()
        cid_count=cart.objects.filter(user=uid).count()

        search_query = request.GET.get('query')
        if search_query:
            pid = pid.filter(name__icontains=search_query)
        contaxt={
            "cid":cid,
            "pid":pid,
            "uid":uid,
            "wid_count": wid_count,
            "cid_count": cid_count,
            "search_query": search_query,
        }
        return render(request,"index.html",contaxt)
    else:
        return redirect(login)
    
def main(request):
    return render(request,"main.html")

def shop_details(request):
    cid=category.objects.all().order_by("-id")
    pid=product.objects.all().order_by("-id")
    uid=user.objects.get(username=request.session['username'])
    wid_count=wishlist.objects.filter(user=uid).count()
    cid_count=cart.objects.filter(user=uid).count()
    contaxt={
            "cid":cid,
            "pid":pid,
            "uid":uid,
            "wid_count": wid_count,
            "cid_count": cid_count,
        }
    return render(request,"shop_details.html", contaxt)

# from django.core.paginator import Paginator
# from .models import category, product  # Adjust imports as needed

# def shop_grid(request):
#     cid = category.objects.all().order_by("-id")

#     # Get filters from GET parameters
#     cate = request.GET.get("cate")
#     min_price = request.GET.get("min_price")
#     max_price = request.GET.get("max_price")

#     # Base queryset
#     pid = product.objects.all()

#     # Filter by category if provided
#     if cate:
#         pid = pid.filter(category=cate)

#     # Filter by price range if provided
#     if min_price:
#         pid = pid.filter(price__gte=min_price)
#     if max_price:
#         pid = pid.filter(price__lte=max_price)

#     # Order by latest
#     pid = pid.order_by("-id")

#     # Pagination (10 per page)
#     pagination = Paginator(pid, 10)
#     page = request.GET.get("page")
#     pid = pagination.get_page(page)

#     # Pass filter values to template for preserving state
#     context = {
#         "cid": cid,
#         "pid": pid,
#         "cate": cate,
#         "min_price": min_price,
#         "max_price": max_price,
#     }

#     return render(request, "shop_grid.html", context)

def shop_grid(request):
    cid = category.objects.all().order_by("-id")
    uid=user.objects.get(username=request.session['username'])
    wid_count=wishlist.objects.filter(user=uid).count()
    cid_count=cart.objects.filter(user=uid).count()
    wishlist_items = []
    
    # Get wishlist items if user is logged in
    if 'username' in request.session:
        uid = user.objects.get(username=request.session['username'])
        wishlist_items = wishlist.objects.filter(user=uid).values_list('product_id', flat=True)
    
    # Get price filter parameters
    min_price = request.GET.get('min_price', '').replace('$', '')
    max_price = request.GET.get('max_price', '').replace('$', '')
    
    # Base queryset
    pid = product.objects.all().order_by("-id")
    
    # Apply price filter if provided
    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            pid = pid.filter(price__gte=min_price, price__lte=max_price)
        except (ValueError, TypeError):
            pass
    
    # Handle category filter
    cate = request.GET.get("cate")
    if cate:
        pid = pid.filter(category=cate)
    
    # Pagination
    pagination = Paginator(pid, 10)
    page = request.GET.get("page")
    pid = pagination.get_page(page)

    context = {
        "cid": cid,
        "pid": pid,
        "uid":uid,
        "wishlist_items": wishlist_items,
        "min_price": min_price if min_price else 10,
        "max_price": max_price if max_price else 540,
        "wid_count":wid_count,
        "cid_count":cid_count,
    }
    return render(request, "shop_grid.html", context)

def shoping_cart(request):
    if 'username' not in request.session:
        return redirect('login')
    
    uid=user.objects.get(username=request.session['username'])
    wid_count=wishlist.objects.filter(user=uid).count()
    cid_count=cart.objects.filter(user=uid).count()
    shop_items = cart.objects.filter(user=uid).select_related('product')
    l1=[i.total_price for i in shop_items]
    sub_total=sum(l1)
    if sub_total == 0:
        shipping=0
    elif sub_total > 99:
        shipping=0
    else:
        shipping=20
    total=sub_total+shipping
    cid=category.objects.all().order_by("-id")

    contaxt={
            "cid":cid,
            "shop_items": shop_items,
            "sub_total": sub_total,
            "shipping": shipping,
            "total": total,
            "wid_count": wid_count,
            "cid_count": cid_count,
        }
    return render(request,"shoping_cart.html", contaxt)

def register(request):
    if request.POST:
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        print(username,email,password1,password2)
        uid=user.objects.filter(email=email).exists()
        user_uid=user.objects.filter(username=username).exists()
        print(uid)
        if user_uid:
            contaxt={
                "msg":"User Exists"
            }
            return render(request, 'register.html',contaxt)
        elif uid:
            contaxt={
                "msg":"Email Exists"
            }
            return render(request, 'register.html',contaxt)
        else:
            if password1 == password2:
                user.objects.create(username=username,email=email,password=password1)
                # return render(request, 'register.html')
                contaxt = {
                    "msg": "Registration successful! Please log in."
                }
                return redirect('login')
            else:
                contaxt={
                    "msg":"Password Not match"
                }
                return render(request, 'register.html',contaxt)
    return render(request, 'register.html')


def login(request):
    if "username" in request.session:
        return redirect(index)
    else:
        if request.POST:
            username=request.POST['username']
            password=request.POST['password']
            print(username,password)
            user_uid=user.objects.filter(username=username).exists()
            if user_uid:
                user_uid=user.objects.get(username=username)
                if user_uid.password == password:
                    request.session["username"]=user_uid.username
                    return redirect(index)
                else:
                    contaxt={
                            "msg":"Password Not exists "
                        }
                    return render(request,"login.html",contaxt)
            else:
                contaxt={
                        "msg":"User Not exists. Please register first. "
                    }
                return render(request,"login.html",contaxt)
    return render(request,"login.html")

def logout(request):
    del request.session['username']
    return redirect(login)

def profile(request):
    uid=user.objects.get(username=request.session['username'])
    print(uid)
    if request.POST:
        username=request.POST['username']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        if request.FILES:
            image=request.FILES['image']
            uid.username=username
            uid.email=email
            uid.phone_number=phone_number
            uid.image=image
            uid.save()
        else:
            uid.username=username
            uid.email=email
            uid.phone_number=phone_number
            uid.save()
        request.session["username"]=uid.username    
    con={
        "uid":uid
    }
    return render(request, 'profile.html',con)

import random
def f_password(request):
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1000,9999)
        print(email)
        uid=user.objects.filter(email=email).exists()
        if uid:
            send_mail("test",f"have a nice day {otp}","namanjain3534@gmail.com",[email])
            uid=user.objects.get(email=email)
            uid.otp=otp
            uid.save()
            con={
                "uid":uid
            }
            return render(request, 'confirm_password.html',con)
        else:
            con={
                "msg":"Invalid Email"
            }
            return render(request, 'f_password.html',con)

    return render(request, 'f_password.html')

def confirm_password(request):
    if request.method == 'POST':
        email=request.POST['email']
        otp=request.POST['otp']
        new_password=request.POST['new_password']
        confirm_password1=request.POST['confirm_password']
        print(email,otp,new_password,confirm_password)
        uid=user.objects.get(email=email)
        print(type(uid.otp),type(otp))
        if uid.otp == int(otp):
            print("okokok")
            if new_password == confirm_password1:
                uid.password=new_password
                uid.save()
                return redirect(login)
            else:
                contaxt={
                    "msg":"Password Not match",
                    "uid":uid
                }
                return render(request, 'confirm_password.html',contaxt)
        else:
            contaxt={
                "msg":"Invalid OTP",
                "uid":uid
            }
            return render(request, 'confirm_password.html',contaxt)    
    else:
        return render(request,"confirm_password.html")
    
        # if not user.objects.filter(email=email).exists():
        #     contaxt={
        #         "msg":"Email not register"
        #     }
        #     return render(request, 'confirm_password',contaxt)
        
        # otp_r=OTPModel.objects.filter(email=email,otp=otp).first()
        # if not otp_r:
        #     contaxt={
        #         "msg":"Invalid OTP"
        #     }
        #     return render(request, 'register.html',contaxt)
        
        # if new_password != confirm_password:
        #     contaxt={
        #         "msg":"Password Not match"
        #     }
        #     return render(request, 'confirm_password.html',contaxt)
            
        # user = User.objects.get(email=email)
        # user.password = make_password(new_password)
        # user.save()    

        # otp_r.delete()
        # con={
        #     "msg":"Password successfully updated. You can now log in."
        # }
        # return render(request,"login.html",con)
    #     return render(request,"confirm_password.html")

    
    # return render(request,"confirm_password.html")



def search_fun(request):
    search=request.GET.get('search')
    print("abcd",search)
    pid=product.objects.filter(name__contains=search)
    contaxt={
        "pid":pid
    }
    return render(request,"shop_grid.html",contaxt)


# def add_wishlist(request,id):
#     uid=user.objects.get(username=request.session['username'])
#     pid=product.objects.get(id=id)
#     wid_exists=wishlist.objects.filter(user=uid,product=pid)
#     if wid_exists:
#         wid_exists=wishlist.objects.get(user=uid,product=pid).delete()
#         return redirect(shop_grid)
#     else:
#         wishlist.objects.create(user=uid,product=pid)
#         return redirect(shop_grid)

# def wishlists(request):
#     return render(request,"wishlist.html")

def add_wishlist(request, id):
    if 'username' not in request.session:
        return redirect('login')  # Not logged in

    uid = user.objects.get(username=request.session['username'])
    pid = product.objects.get(id=id)

    existing = wishlist.objects.filter(user=uid, product=pid)
    if existing.exists():
        existing.delete()  # Remove from wishlist
    else:
        wishlist.objects.create(user=uid, product=pid)  # Add to wishlist
    referer = request.META.get('HTTP_REFERER', '')

    # Case 1: If user came from wishlists page and it's now empty → go to shop_grid
    if 'wishlists' in referer and not wishlist.objects.filter(user=uid).exists():
        return redirect('shop_grid')

    # Case 2: Otherwise, return to the page user came from (shop_grid, product page, etc.)
    return redirect(referer or 'shop_grid')
    # return redirect('wishlists')  # Or use request.META.get('HTTP_REFERER') to go back to same page


def wishlists(request):
    uid=user.objects.get(username=request.session['username'])
    wid_count=wishlist.objects.filter(user=uid).count()
    cid_count=cart.objects.filter(user=uid).count()
    wishlist_items = wishlist.objects.filter(user=uid)
    contaxt={
        "wid_count":wid_count,
        "cid_count":cid_count,
        "uid":uid,
        "wishlist_items":wishlist_items
    }
    return render(request, "wishlist.html", contaxt)

def add_cart(request,id):
    if 'username' not in request.session:
        return redirect('login')  # Not logged in

    uid = user.objects.get(username=request.session['username'])
    pid = product.objects.get(id=id)

    existing = cart.objects.filter(user=uid, product=pid)
    if existing.exists():
        existing.delete()  # Remove from cart
    else:
        cart.objects.create(user=uid, product=pid,qty=1,total_price=pid.price)  # Add to cart

    # return redirect('shop_grid')  # Or use request.META.get('HTTP_REFERER') to go back to same page
    referer = request.META.get('HTTP_REFERER', '')
    if 'shoping_cart' in referer:
        return redirect('shoping_cart')  # your cart page URL name
    else:
        return redirect('shop_grid')  # fallback if not from cart
    
def cart_plus(request,id):
    cid=cart.objects.get(id=id)
    cid.qty+=1
    cid.total_price=cid.product.price*cid.qty
    cid.save()
    return redirect(shoping_cart)

def cart_minus(request,id):
    cid=cart.objects.get(id=id)
    if cid.qty>1:
        cid.qty-=1
        cid.total_price=cid.product.price*cid.qty
        cid.save()
    else:
        cid.delete()
    return redirect(shoping_cart)
import uuid
def Add_Billing(request):
    if 'username' not in request.session:
        return redirect('login')

    uid = user.objects.get(username=request.session['username'])
    wid_count = wishlist.objects.filter(user=uid).count()
    cid_count = cart.objects.filter(user=uid).count()
    cid = cart.objects.filter(user=uid)
    subtotal=sum([i.total_price for i in cid])
    
    if request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        country = request.POST['country']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        phone_number = request.POST['phone_number']
        email = request.POST['email']

        Billing_details.objects.create(
            user=uid,
            first_name=first_name,
            last_name=last_name,
            country=country,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone_number=phone_number,
            email=email
        )
        messages.success(request, "Billing details saved successfully.")
        latest_address=Billing_details.objects.filter(user=uid).order_by("-id")[0]
        order_id = str(uuid.uuid4()).replace('-', '')[:12]
        oid=order.objects.create(user=uid,address=latest_address,subtotal=subtotal,total=subtotal,order_id=order_id)
        oid.product.set(cid)
        return redirect('checkout')

    context = {
        "uid": uid,
        "wid_count": wid_count,
        "cid_count": cid_count
    }
    return render(request, 'checkout.html', context)

def order_detail(request):
    if 'username' not in request.session:
        return redirect('login')

    uid = user.objects.get(username=request.session['username'])
    orders = order.objects.filter(user=uid).order_by('-datetime')

    contaxt = {
        "orders": orders,
    }
    return render(request, 'order_list.html', contaxt)

def single_orders (request,id):
    oid=order.objects.get(id=id)
    uid=user.objects.get(username=request.session['username'])
    wid_count=wishlist.objects.filter(user=uid).count()
    cid_count=cart.objects.filter(user=uid).count()
    con={
        "oid":oid,
        "uid":uid,
        "wid_count":wid_count,
        "cid_count":cid_count,
    }
    return render (request, "single_order.html",con)