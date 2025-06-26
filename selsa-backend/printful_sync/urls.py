# urls.py

from django.urls import path
from printful_sync.views import sync_printful_view, list_stores_view, debug_store_view, test_store_exists  # ✅ Import the new view

urlpatterns = [
    path("sync-printful/", sync_printful_view),
    path('list-stores/', list_stores_view),
    path('debug-store/', debug_store_view),  # ✅ Add this
    path('test-store/', test_store_exists),
]
