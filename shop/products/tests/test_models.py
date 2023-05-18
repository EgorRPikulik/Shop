import datetime as dt

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from products.models import Product, Category


class TestModels(TestCase):
    fixtures = ['users.json']
    
    def setUp(self) -> None:
        self.user = User.objects.get(username='admin')
        self.product1 = Product.objects.create(
            name='холодильник',
            info='the best holodos',
            image_url='some_name.jpg',
            category = Category.objects.create(name='бытовая техника')
        )

        
        return super().setUp()
    
    def test_product_is_assigned_default_quantity_on_creation(self):
        self.assertEquals(self.product1.quantity, 0)

    def test_product_is_assigned_default_price_on_creation(self):
        self.assertEquals(self.product1.price, .0)

        
        
    def test_unique_product_name(self):
        with self.assertRaises(IntegrityError):
            product2 = Product.objects.create(
                name='холодильник',
                info='the best holodos',
                image_url='2.jpg',
                price=12.0,
                category = Category.objects.create(name='бытовая техника')
            )
            
    def test_unique_image_url(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name='some',
                info='the best holodos',
                image_url='some_name.jpg',
                price=12.0,
                category = Category.objects.create(name='бытовая техника')
            )
         
        