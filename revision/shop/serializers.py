from rest_framework.serializers import ModelSerializer, SerializerMethodField

from shop.models import Category, Product, Article


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'product', 'date_created', 'date_updated']


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'date_created', 'date_updated']

class ProductDetailSerializer(ModelSerializer):

    articles = SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'date_created', 'date_updated', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated']

class CategoryDetailSerializer(ModelSerializer):

    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'products'] # to display fileds

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data