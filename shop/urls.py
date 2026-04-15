from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('product/<int:pk>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.order_create, name='checkout'),
    
    # Comparison URLs
    path('compare/', views.compare_list, name='compare_list'),
    path('compare/add/<int:product_id>/', views.compare_add, name='compare_add'),
    path('compare/remove/<int:product_id>/', views.compare_remove, name='compare_remove'),
    path('compare/clear/', views.compare_clear, name='compare_clear'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='shop:product_list'), name='logout'),
    path('register/', views.register, name='register'),
]
