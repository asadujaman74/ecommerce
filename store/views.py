from django.shortcuts import render
from . models import Category, Product
from django.shortcuts import get_object_or_404 #FOR INDIVISUAL PRODUCT / category SHOWN


#home and all product views
def store(request):
    all_products = Product.objects.all()
    context = {'my_product': all_products}
    return render (request, 'store/store.html', context)


#categories context proccesor for all pages
def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

#indivisual category views
def list_category(request, category_slug = None):
    category = get_object_or_404(Category, slug = category_slug)
    products = Product.objects.filter(category=category)
    context = {
        'category':category,
        'products':products
        }
    return render(request, 'store/list-category.html', context)

#Single / indivisual product views
def product_info(request,product_slug):
    product = get_object_or_404(Product, slug = product_slug)
    context = {'product':product}
    return render(request, 'store/product-info.html', context)



