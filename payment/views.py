from django.shortcuts import render
from . models import ShippingAddress , Order , OrderItem
from cart.cart_session import Cart
from django.http import JsonResponse
# Create your views here.

def checkout(request):

    # User with logged in account -- prefilled 
    if request.user.is_authenticated:
        try:
            # Authenticated user with shipping information 
            shipping_address = ShippingAddress.objects.get(user = request.user.id)

            context = {'shipping': shipping_address}
            return render(request, 'payment/checkout.html', context=context)
        except:
            # Authenticated user with NO shipping information
            return render(request, 'payment/checkout.html')
    
    else:
        # Guest User
        return render(request, 'payment/checkout.html')
    

def complete_order(request):

    # ✔️ Step 1: Check request method POST কিনা

    if request.POST.get('action') == 'post':

         # ✔️ Step 2: AJAX থেকে কোন কোন data আসছে তা ধরার জন্য request.POST.get()
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')

        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # grab user shipping address at one place
        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode )

        # shopping cart information
        cart = Cart(request)

        # get total pice in item
        total_cost = cart.get_total()

        '''
            Order - Variation

            1) Create order -> Account User With + Without shipping information
            2) Create order -> Guest users without an account 
        '''
        # 1) Create order -> Account User With + Without shipping information
        if request.user.is_authenticated:

            order = Order.objects.create(
                full_name = name,
                email = email,
                shipping_address = shipping_address,
                amount_paid = total_cost,
                user = request.user,
            )

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(

                    order_id = order_id, 
                    product = item['product'],
                    quantity = item['qty'],
                    price = item['price'],
                    user = request.user,

                    )
        # 2) Create order -> Guest users without an account
        else:
        
            order = Order.objects.create(full_name = name,email = email,
            shipping_address = shipping_address,amount_paid = total_cost)

            order_id = order.pk

            for item in cart:
        
                OrderItem.objects.create(order_id = order_id, product = item['product'],quantity = item['qty'],price = item['price'])
        
        order_success = True
        response = JsonResponse({'success': order_success})
        return response



def payment_success(request):

    # clear shopping cart
    for key in list(request.session.keys()):
        if key == 'cart':
            del request.session[key]

    request.session.modified = True


    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')
