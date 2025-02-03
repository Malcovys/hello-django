from rest_framework import serializers

from shop.models import Category, Product, Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'product', 'date_created', 'date_updated']
    
    def validate_price(self, value):
        if value <= 1:
            raise serializers.ValidationError('Price must be greater than 1')
        return value

    def validate_product(self, value):
        if not value.active:
            raise serializers.ValidationError('Product is not active')
        return value


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'date_created', 'date_updated', 'ecoscore']

class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'date_created', 'date_updated', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'description']
    
    def validate_name(self, value): # Validation d'un champ
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value
    
    def validate(self, data): # Validation multiple
        if data['name'] not in data['description']:
            raise serializers.ValidationError("Name must be in description")
        return data

class CategoryDetailSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'products'] # to display fileds

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data