from django.shortcuts import render
from category.models import Category
from store.models import Product, ReviewRating




def index(request):

    products = Product.objects.all().filter(is_available=True).order_by("-created")

    # Get the reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

 
    return render(request, "commerce/index.html", {
        "products": products,
        "reviews": reviews,
    })