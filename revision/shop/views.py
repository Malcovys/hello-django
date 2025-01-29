
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import Category, Product, Article

from shop.serializers import ArticleSerializer
from shop.serializers import ProductListSerializer, ProductDetailSerializer
from shop.serializers import CategoryListSerializer, CategoryDetailSerializer


### ReadOnly
class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer # par défaut
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)
    
    @action(detail=True, methods=['post']) # detail=True -> utilisable que sur une category existante
    def disable(self, request, pk):
        self.get_object().disable()  # sef.get_object() -> instance de Category / Category courrante
        return Response()
    
class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

class ArticleViewset(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product=product_id)
        return queryset

### Admin   
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.all()

class AdminArticleViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()