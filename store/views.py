from django.shortcuts import render, get_list_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from orders.models import OrderProduct
from .forms import ReviewForm
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator    #for pagination 
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404




def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_list_or_404(Category, slug=category_slug)
        # Assuming you want to get the first category from the list
        category = categories[0] if categories else None
        products = Product.objects.filter(category=category, is_available=True)
        paginator = Paginator(products, 6) #show 4 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.filter(is_available=True).order_by("id") #get all the products
        paginator = Paginator(products, 6) #show 4 products per page
        page = request.GET.get('page')  #get the page number
        paged_products = paginator.get_page(page)   #get the products for the page number

    return render(request, "store/store.html", {
        "products": paged_products,
        "categories": categories,
        "products_count": products.count(),
    })



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() #check if the product is already in the cart or not

    except Exception as e:
        raise e

    try:
        # Check if the user is authenticated before accessing the user object
        if request.user.is_authenticated:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        else:
            orderproduct = None

    except OrderProduct.DoesNotExist:
        orderproduct = None


    #get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    #get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    
    return render(request, "store/product_detail.html", {
        "single_product": single_product,
        "in_cart": in_cart,
        "orderproduct": orderproduct,
        "reviews": reviews,
        "product_gallery": product_gallery,
    })



def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created").filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            product_count = products.count()
    return render(request, "store/store.html", {
        "products": products,
        "product_count": product_count,
    })




def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER") #get the last url

    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)    