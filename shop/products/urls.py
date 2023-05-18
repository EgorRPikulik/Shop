from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    path('', list_products, name = 'list_products'),
    path('<int:id>/', product_details, name = 'product_details'),
    path('create/', create_product, name = 'create_product'),
    path('category/create/', create_category, name='create_category'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/delete/<int:product_id>/', delete_from_cart, name = 'delete_from_cart'), 
    path('cart/', my_cart, name = 'my_cart'),
    path('cart/payment/<int:card_id>', payment, name = 'payment'),
    path('card/add/', add_card, name='add_card'),
    path('card/', my_cards, name='my_cards'),
    path('card/select/', select_card_for_payment, name='select_card_for_payment'),
    path('card/delete/<int:card_id>', delete_card, name='delete_card'),
    path('purchases/', list_purchases, name='list_purchases')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
