from django.db import models, transaction
import requests


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @transaction.atomic
    def disable(self):
        if self.active is False:
            return
        self.active = False
        self.save()
        self.products.update(active=False)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def call_external_api(self, method, url):
        return requests.request(method, url)
    
    @property
    def ecoscore(self):
        response = self.call_external_api('GET', 'https://world.openfoodfacts.org/api/v0/product/3229820787015.json')
        if response.status_code == 200:
            return response.json()['product']['ecoscore_grade']
    
    @transaction.atomic
    def disable(self):
        if self.active is False:
            return
        self.active = False
        self.save()
        self.articles.update(active=False) # Article est lié à produit pas une clé étrangère


class Article(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name