from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem
from .forms import OrderCreateForm

@login_required
def order_create(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('shop:product_list')
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for product_id, item in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item['price'],
                        quantity=item['quantity']
                    )
                except Product.DoesNotExist:
                    continue
            # Clear the cart
            request.session['cart'] = {}
            return render(request, 'shop/order_success.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    # Calculate cart total for display
    cart_items = []
    total_price = 0
    to_remove = []
    
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = int(item['price']) * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': item_total
            })
            total_price += item_total
        except Product.DoesNotExist:
            to_remove.append(product_id)

    if to_remove:
        for pid in to_remove:
            if pid in cart:
                del cart[pid]
        request.session['cart'] = cart
        request.session.modified = True
        if not cart:
            return redirect('shop:product_list')
        
    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        queryset = Product.objects.filter(available=True)
        
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
            
        # Tìm kiếm
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        # Lọc theo giá
        price_filter = self.request.GET.get('price')
        if price_filter == 'under_5m':
            queryset = queryset.filter(price__lt=5000000)
        elif price_filter == '5m_15m':
            queryset = queryset.filter(price__gte=5000000, price__lte=15000000)
        elif price_filter == 'over_15m':
            queryset = queryset.filter(price__gt=15000000)
            
        # Sắp xếp
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-created')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_price_filter'] = self.request.GET.get('price')
        context['current_sort'] = self.request.GET.get('sort')
        context['current_search'] = self.request.GET.get('search')
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
    
    # Lấy số lượng từ request, mặc định là 1
    try:
        quantity = int(request.GET.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    if product_id not in cart:
        product = get_object_or_404(Product, id=product_id)
        cart[product_id] = {'quantity': 0, 'price': str(product.price)}
    
    # Nếu là cập nhật số lượng trực tiếp (từ trang giỏ hàng)
    if request.GET.get('update'):
        cart[product_id]['quantity'] = quantity
    else:
        # Nếu là thêm vào giỏ (từ trang chi tiết)
        cart[product_id]['quantity'] += quantity
        
    request.session['cart'] = cart
    
    # Nếu là mua ngay thì chuyển hướng đến checkout, ngược lại về giỏ hàng
    if request.GET.get('buy_now'):
        return redirect('shop:checkout')
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    # Danh sách các ID cần xóa nếu không tìm thấy sản phẩm
    to_remove = []
    
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = int(item['price']) * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': item_total
            })
            total_price += item_total
        except Product.DoesNotExist:
            to_remove.append(product_id)
            
    # Xóa các sản phẩm không còn tồn tại khỏi session
    if to_remove:
        for pid in to_remove:
            if pid in cart:
                del cart[pid]
        request.session['cart'] = cart
        request.session.modified = True
    
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

# --- Logic So sánh sản phẩm (Comparison System) ---
def compare_add(request, product_id):
    compare = request.session.get('compare', [])
    product_id = int(product_id)
    if product_id not in compare:
        if len(compare) >= 3:
            compare.pop(0) # Chỉ cho phép so sánh tối đa 3 sản phẩm
        compare.append(product_id)
        request.session['compare'] = compare
    return redirect('shop:compare_list')

def compare_list(request):
    compare_ids = request.session.get('compare', [])
    products = Product.objects.filter(id__in=compare_ids)
    
    # Sắp xếp lại theo thứ tự đã thêm
    sorted_products = []
    for pid in compare_ids:
        for p in products:
            if p.id == pid:
                sorted_products.append(p)
                break

    # Lấy tất cả các key thông số kỹ thuật duy nhất từ các sản phẩm
    all_spec_keys = []
    for p in sorted_products:
        for key in p.specifications.keys():
            if key not in all_spec_keys:
                all_spec_keys.append(key)

    return render(request, 'shop/compare.html', {
        'products': sorted_products,
        'all_spec_keys': all_spec_keys
    })

def compare_remove(request, product_id):
    compare = request.session.get('compare', [])
    product_id = int(product_id)
    if product_id in compare:
        compare.remove(product_id)
        request.session['compare'] = compare
    return redirect('shop:compare_list')

def compare_clear(request):
    request.session['compare'] = []
    return redirect('shop:product_list')
