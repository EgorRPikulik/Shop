from django.test import SimpleTestCase
from django.urls import reverse, resolve

from products.views import *


class TestUrls(SimpleTestCase):
    def test_list_products_url_resolves(self):
        url = reverse('list_products')
        self.assertEquals(resolve(url).func, list_products)
        
    def test_product_details_url_resolves(self):
        url = reverse('product_details', args=(1,))
        self.assertEquals(resolve(url).func, product_details)
        
    def test_add_to_cart_url_resolve(self):
        url = reverse('add_to_cart', args=(1,))
        self.assertEquals(resolve(url).func, add_to_cart)
        
    def test_my_cart_url_resolves(self):
        url = reverse('my_cart')
        self.assertEquals(resolve(url).func, my_cart)
        
    def test_delete_from_cart_url_resolves(self):
        url = reverse('delete_from_cart', args=(1,))
        self.assertEquals(resolve(url).func, delete_from_cart)
        
    def test_create_product_url_resolve(self):
        url = reverse('create_product')
        self.assertEquals(resolve(url).func, create_product)
        
        
    def test_create_category_url_resolves(self):
        url = reverse('create_category')
        self.assertEquals(resolve(url).func, create_category)

    def test_delete_product_url_resolves(self):
        url = reverse('delete_product', args=(1,))
        self.assertEquals(resolve(url).func, delete_product)
        
    def test_add_card_url_resolve(self):
        url = reverse('add_card')
        self.assertEquals(resolve(url).func, add_card)
    def test_my_cards_url_resolve(self):
        url = reverse('my_cards')
        self.assertEquals(resolve(url).func, my_cards)

    def test_delete_card_url_resolve(self):
        url = reverse('delete_card', args=(1,))
        self.assertEquals(resolve(url).func, delete_card)
        
    def test_select_card_for_payment_url_resolve(self):
        url = reverse('select_card_for_payment')
        self.assertEquals(resolve(url).func, select_card_for_payment)
        
    def test_payment_url_resolve(self):
        url = reverse('payment',args=(1,))
        self.assertEquals(resolve(url).func, payment)

    def test_list_purchases_url_resolve(self):
        url = reverse('list_purchases')
        self.assertEquals(resolve(url).func, list_purchases)
  
        
        