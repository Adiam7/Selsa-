# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django_cas_ng import views as cas_views
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    # CHANGED: Now all app APIs are nested under /api/
    path('api/categories/', include('category.urls')),  
    path('api/products/', include('products.urls')),     
    path('api/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('', include('printful_sync.urls')),  # New Printful sync endpoint
    
    # Other non-API views
    path('', include('pages.urls')),  
    path('api/', include('accounts.urls')),  
    path('accounts/', include('social_django.urls', namespace='social')),  
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/templates/registration/login/', cas_views.LoginView.as_view(), name='cas_login'),
    path('auth/templates/registration/logout/', cas_views.LogoutView.as_view(), name='cas_logout'),
    path('', include(tf_urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
