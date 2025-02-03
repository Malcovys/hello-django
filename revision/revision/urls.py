from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shop.views import CategoryViewset, ProductViewset, ArticleViewset
from shop.views import AdminCategoryViewset, AdminArticleViewset

router = routers.SimpleRouter()

# ReadOnly
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('article', ArticleViewset, basename='article')

# Admin
router.register('admin/category', AdminCategoryViewset, basename='category-admin')
router.register('admin/article', AdminArticleViewset, basename='article-admin')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]
