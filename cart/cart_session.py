from decimal import Decimal
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session

        # Try to get an existing cart
        cart = self.session.get('cart')

        # If not exist, create a new one
        if not cart:
            cart = self.session['cart'] = {}

        # Make it available as instance variable
        self.cart = cart

    def add(self, product, product_qty):
        # ✅ Correct: access product.id, not productid or product_id undefined
        product_id = str(product.id)

        if product_id in self.cart:
            # Update quantity if already in cart
            self.cart[product_id]['qty'] = product_qty
        else:
            # Add new product
            self.cart[product_id] = {
                'price': str(product.price),
                'qty': product_qty
            }

        # Mark session as modified so Django saves it
        self.session.modified = True


    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        all_prodict_ids = self.cart.keys()

        products = Product.objects.filter(id__in = all_prodict_ids)

        cart = self.cart.copy()

        for product in products:

            cart [str(product.id)] ['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])

            item['total'] = item['price'] * item['qty']

            yield item

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
    

    # delete product button from session
    def delete(self,product):
        product_id = str(product)   #grap perticular product
        
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True

    # update product button from session
    def update(self, product, qty):

        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
        
        self.session.modified = True


