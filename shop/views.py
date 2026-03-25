from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Category, Product

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            return Product.objects.filter(category=self.category, available=True)
        return Product.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['category'] = self.category
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

# --- Logic Giỏ hàng (Cart System) ---
def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id not in cart:
        cart[product_id] = {'quantity': 0, 'price': str(Product.objects.get(id=product_id).price)}
    
    # Giả sử mặc định cộng thêm 1
    cart[product_id]['quantity'] += 1
    request.session['cart'] = cart
    return redirect('shop:product_list')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = int(item['price']) * item['quantity']
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': item['price'],
            'total_price': item_total
        })
        total_price += item_total
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
    return redirect('shop:cart_detail')
