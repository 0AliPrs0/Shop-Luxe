"""
URL configuration for shop_luxe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from accounts import views as accounts_views
from products import views as products_views
from product_reviews import views as product_rewiews_view
from orders import views as orders_views
from cart import views as cart_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/register/', accounts_views.UserRegistrationView.as_view(), name='user-register'),
    path('api/auth/login/', accounts_views.UserLoginView.as_view(), name='user-login'),
    path('api/auth/logout/', accounts_views.UserLogoutView.as_view(), name='user-logout'),
    path('api/auth/password-reset/', accounts_views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('api/auth/password-reset/confirm/', accounts_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('api/profile/me/', accounts_views.UserProfileView.as_view(), name='user-profile'),
    path('api/products/', products_views.ProductListView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', products_views.ProductDetailView.as_view(), name='product-detail'),
    path('api/categories/', products_views.CategoryListView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', products_views.CategoryDetailView.as_view(), name='category-detail'),
    path('api/products/<int:product_id>/reviews/', product_rewiews_view.ReviewListView.as_view(), name='product-reviews'),
    path('api/products/<int:product_id>/reviews/add/', product_rewiews_view.ReviewCreateView.as_view(), name='add-review'),
    path('api/orders/', orders_views.OrderListView.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', orders_views.OrderDetailView.as_view(), name='order-detail'),
    path('api/payments/initiate/', orders_views.InitiatePaymentView.as_view(), name='initiate-payment'),
    path('api/payments/callback/', orders_views.PaymentCallbackView.as_view(), name='payment-callback'),
    path('api/search/', products_views.GlobalSearchView.as_view(), name='global-search'),
    path('api/cart/', cart_views.CartDetailView.as_view(), name='user-cart'),
    path('api/cart/add/', cart_views.AddToCartView.as_view(), name='add-to-cart'),
    path('api/cart/update/<int:pk>/', cart_views.UpdateCartItemView.as_view(), name='update-cart-item'),
    path('api/cart/remove/<int:pk>/', cart_views.RemoveFromCartView.as_view(), name='remove-from-cart'),

]
