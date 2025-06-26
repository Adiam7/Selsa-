# pages/urls.py

from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),           # Homepage
    path('about/', views.about, name='about'),       # About page
    path('contact/', views.contact, name='contact'), # Contact page
    path('services/', views.services, name='services'), # Services page
    path('coming_soon/', views.coming_soon, name='coming_soon'), # Coming soon page
    path('clothing/', views.clothing, name='clothing'), # Clothing page
    path('new_collection/', views.new_collection, name='new_collection'), # New collection page
    path('delivery/', views.delivery, name='delivery'), # Delivery page
    path('products/', views.products, name='products'), # Products page
    path('intro/', views.intro, name='intro'), # Introduction page
    
    # path('privacy/', views.privacy, name='privacy'), # Privacy page
    # path('terms/', views.terms, name='terms'), # Terms page
    # path('faq/', views.faq, name='faq'), # FAQ page
    # path('support/', views.support, name='support'), # Support page
    # path('blog/', views.blog, name='blog'), # Blog page
    # path('blog_post/', views.blog_post, name='blog_post'), # Blog post page
    # Add more global pages as needed
    
]
