# urls.py
from django.urls import path
from .views import ProductsByDivision,ProductDetails,CalculateLotDetails
from .addtocart import AddToCart,CartDetailsView
from .Custlogin import CustomerauthLoginView
from .placeorder import PlaceOrder
from .CreditPayment import CreditPaymentOrders_DispatchedListView
from .customerDetails import DispatchCustomerDetails,PendingCustomerDetails,DeliveredCustomerDetails,InprocessCustomerDetails
from .Lr_verify import LRVerificationAPI
from .cust_OrderInvoice_views import GenerateInvoiceAPI
from .deleteproduct import DeleteProduct
from .order_Status import GetPendingOrders,InprocessOrders,DispatchOrders,DeliveredOrders,CancelledOrders



urlpatterns = [
    path('get-products-by-division/', ProductsByDivision.as_view(), name='get-products-by-division'),
    path('get-products-details/', ProductDetails.as_view(), name='get-products-details'),
    path('calculate-margin/', CalculateLotDetails.as_view(), name='calculate-margin'),
    path('addto-cart/', AddToCart.as_view(), name='addto-cart'),
    path('cart-details/', CartDetailsView.as_view(), name='cart-details'),
    path('customer/login/', CustomerauthLoginView.as_view(), name='customer_login'),
    path('placeorder/', PlaceOrder.as_view(), name='placeorder'),
    path('credit-payment-orders/', CreditPaymentOrders_DispatchedListView.as_view(), name='credit_payment_orders'),
    path('lr-verification/', LRVerificationAPI.as_view(), name='lr-verification'),
    path('generate-invoice/', GenerateInvoiceAPI.as_view(), name='lr-verification'),
    path('delete-product/<int:order_product_id>/', DeleteProduct.as_view(), name='delete_product'),
    path('orders/pending/', GetPendingOrders.as_view(), name='get_pending_orders'),
    path('orders/inprocess/', InprocessOrders.as_view(), name='get_inprocess_orders'),
    path('orders/dispatch/', DispatchOrders.as_view(), name='get_dispatch_orders'),
    path('orders/delivered/', DeliveredOrders.as_view(), name='get_delivered_orders'),   
    path('orders/cancelled/', CancelledOrders.as_view(), name='get_cancelled_orders'),     
    path('order/dispatch/details/', DispatchCustomerDetails.as_view(), name='order_dispatch_details'),  
    path('order/inprocess/details/', InprocessCustomerDetails.as_view(), name='order_inprocess_details'),  
    path('order/delivered/details/', DeliveredCustomerDetails.as_view(), name='order_delivered_details'), 
    path('order/pending/details/', PendingCustomerDetails.as_view(), name='order_pending_details'), 
    path('customer_order_invoice_dispatch/', GenerateInvoiceAPI.as_view(), name='customer_details'),













]

    