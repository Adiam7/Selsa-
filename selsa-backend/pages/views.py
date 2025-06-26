# Create your views here.
# pages/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'pages/index.html')  # Template path relative to your templates directory

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

def services(request):
    return render(request, 'pages/services.html')

def coming_soon(request):
    return render(request, 'pages/coming_soon.html')

def clothing(request):
    return render(request, 'pages/clothing.html')

def new_collection(request):
    return render(request, 'pages/new_collection.html')

def delivery(request):
    return render(request, 'pages/delivery.html')

def products(request):
    return render(request, 'pages/products.html')

def intro(request):
    return render(request, 'pages/intro.html')

# def privacy(request):
#     return render(request, 'pages/privacy.html')

# def terms(request):
#     return render(request, 'pages/terms.html')

# def faq(request):
#     return render(request, 'pages/faq.html')

# def support(request):
#     return render(request, 'pages/support.html')

# def blog(request):
#     return render(request, 'pages/blog.html')