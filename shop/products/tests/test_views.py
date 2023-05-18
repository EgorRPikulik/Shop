import datetime as dt

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestView(TestCase):
    
    fixtures = ['users.json']
    
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='admin')
        return super().setUp()
    
    
    def test_product_list_GET(self):
        response = self.client.get(reverse('list_products'))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_products.html')
        
        
    def test_create_product_page_by_admin(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('create_product'))
        
        self.assertEquals(response.status_code, 200)

    def test_create_product_page_by_user(self):
        self.client.login(username='user', password='user1234')
        response = self.client.get(reverse('create_product'))
        
        self.assertEquals(response.status_code, 403)
      
        
    
        
    def test_login_required_my_cart_page(self):
        response = self.client.get(reverse('my_cart'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'my_cart.html')

        
        self.client.login(username='user', password='user1234')
        response = self.client.get(reverse('my_cart'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_cart.html')


    def test_admin_required_create_product_page(self):
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('create_product'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'create_product.html')

        
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('create_product'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_product.html')
        
        
    def test_login_required_purchases_page(self):
        response = self.client.get(reverse('list_purchases'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'list_purchases.html')

        
        self.client.login(username='user', password='user1234')
        response = self.client.get(reverse('list_purchases'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_purchases.html')
        
        