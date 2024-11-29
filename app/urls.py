from rest_framework import routers
from django.urls import path,include
# from django.conf import settings
# from django.conf.urls.static import static
# from app.authentication import CustomJWTAuthentication
from app.views.COM_OrderDispatchList_views import COMCustomerOrderListDispatchView
from app.views.COM_OrderInprocessList_views import COMCustomerOrderListInprocessView
from app.views.ComCustomerApprovalDetails_views import ComBatchAllocatedDetailsView
from app.views.Com_OrderCustomerInvoice_views import ComBatchAllocatedInvoiceView
from app.views.addtocart import AddToCart
from app.views.placeorder import PlaceOrder
from app.views.CandF_Dropdown_views import CandFDropdownView
from app.views.BatchDropDown_views import BatchDropdownAPIView
from app.views.customerinvoice_views import CustomerinvoiceView
from app.views.CreditPaymentOrders_Dispatched_views import CreditPaymentOrders_DispatchedListView
from app.views.CoeCustomerOnlineOrders_Dispatched_views import CoeCustomerOnlineOrdersDispatchedListView
from app.views.CoeCustomerOnlineOrders_Inprocess_views import CoeCustomerOnlineOrdersInprocessListView
from app.views.PendingPlacedOrderDetails_views import PendingPlacedOrderDetailsView
from app.views.ComCustomerOrders_pending_views import ComPendingCustomerOrderListView
from app.views.ActiveCustomerList_views import ActiveCustomerListView
from app.views.ActiveCustomerDetail_views import ActiveCustomerDetailView
from app.views.Cust_Regist_login_views import CustomerLoginView, CustomerauthLoginView
from app.views.DistributorType_views import DistributorTypeDropdownView
from app.views.StatesDropDown_views import StateDropdownView
from app.views.RolesDropDown_views import CustomerRoleDropdownView
from app.views.cust_views import CustomerRegistrationnewView
from app.views.SupplierDropDown_views import SuppliersDropdownView
from app.views.DivisionsDropDown_views import DivisionDropDownListView
from app.views.CeoCustomerApprovalsDetail_views import CeoCustomerApprovalDetailView
from app.views.AdminCustomerApprovals_views import AdminCustomerApprovalListView
from app.views.AdminCustomerApprovalsDetail_views import AdminCustomerApprovalDetailView
from app.views.CustomerApprovalsDetail_views import CustomerApprovalDetailView
from app.views.FinanceCustomerApprovals_views import CustomerApprovalListView
from app.views.CeoCustomerApprovals_views import CeoCustomerApprovalListView
from app.views.HeadquartersDropDown_views import HeadquartersDropDownListView
from app.views.VzPurchaseReport_view import DeliveryChallanReportView
from app.views.OrderDetailOrderDispatchedView import OrderDetailOrderDispatchedView
from app.views.Vz_Dashboard_views import OrderAndProductDetailsView
#OrderDetailsView,
from app.views.VzRegist_List_view import RegistListVetzoneDetailView
from app.views.VzEnquiry_List_view import VetzoneEnquiryListView, VetzoneEnquiryDetailView
from app.views.Vz_List_view import VetzoneGoodsListAPIView
from app.views.VzEstablishment_List_view import VzEstablishmentListView
from app.views.VzRegist_List_view import VetzoneListView
from app.views.VzOrdersPending_view import VzOrdersPendingView
from app.views.OrderDetailPendingView import OrderDetailView
from app.views.OrderDetailInProcessView import OrderDetailViewInprocess
from app.views.VzOrdersInProcess_view import VzOrdersInProcessView
from app.views.VzOrdersOrdersDispached_view import VzOrdersDispatchedView
from app.views.VzOrdersDelivered_view import VzOrdersDeliveredView
from app.views.VzOrdersCancelled_view import VzOrdersCancelledView
from app.views.OrderDetailDeliveredView import OrderDetailOrderDeliveredView
from app.views.OrderDetailCancelledView import OrderDetailCancelledView
from app.views.VzEstablishPopUp_view import EstablishmentPopupDataView
from app.views.Admin_Regist_login_views import AdminLoginView, RegistrationView, UserLoginView
from app.views.ActiveVetzoneList_views import ActiveVetzoneListView
from app.views.ClosedVetzoneList_views import ClosedVetzoneListView
from app.views.ClosedVzDetails_views import VetzoneClosedDetailView
from app.views.ActiveVzDetails_views import VetzoneActiveDetailView
from app.views.VzCloseRequest_views import VetzoneRemarkUpdateView
from app.views.VzInventory_views import VetZoneProductAvailabilityView
from app.views.VzDropDown_view import VetZoneDropDownView
from app.views.VzQuantity_StockReport_views import DisplayReportView
from app.views.VzAmount_StockReport_views import DisplayReportAmountView
from app.views.VzQandA_StockReport_view import VzQuantityandAmountView
from app.views.views import ProductsByDivision,ProductDetails,CalculateLotDetails

# Registering routers
urlpatterns = [

    #path('Dashboard/', OrderDetailsView.as_view(), name='Dashboard'),#
    path('vetzone-enquiries/', VetzoneEnquiryListView.as_view(), name='vetzone-enquiry-list'),#
    path('vetzone-enquiry/<int:vetzone_id>/', VetzoneEnquiryDetailView.as_view(), name='vetzone-enquiry-detail'),
    path('vetzone-list/', VetzoneGoodsListAPIView.as_view(), name='vetzone-list'),#
    path('establishments/', VzEstablishmentListView.as_view(), name='establishments-list'),#
    path('establishment-popup/<int:vetzone_id>/', EstablishmentPopupDataView.as_view(), name='establishment-popup'),
    path('vetzones-RegistrationList/', VetzoneListView.as_view(), name='vetzoneRegistrationList'),#
    path('vetzone-RegistList-VetzoneDetails/<int:vetzone_id>/', RegistListVetzoneDetailView.as_view(), name='vetzone-RegistList-VetzoneDetails'),
    path('vetzone-orders-pending/', VzOrdersPendingView.as_view(), name='orders-pending'),#
    path('order-details-pending/<int:order_id>/', OrderDetailView.as_view(), name='order-detail-pending'),
    path('vetzone-orders-InProcess/', VzOrdersInProcessView.as_view(), name='orders-Inprocess'),#
    path('order-details-InProcess/<int:order_id>/', OrderDetailViewInprocess.as_view(), name='order-detail-InProcess'),
    path('vetzone-orders-OrdersDispatched/', VzOrdersDispatchedView.as_view(), name='orders-Dispatched'),#
    path('order-details-OrdersDispatched/<int:order_id>/', OrderDetailOrderDispatchedView.as_view(), name='order-detail-OrdersDispatched'),
    path('vetzone-orders-Delivered/', VzOrdersDeliveredView.as_view(), name='orders-Delivered'),#
    path('order-details-Delivered/<int:order_id>/', OrderDetailOrderDeliveredView.as_view(), name='order-detail-OrdersDispatched'), 
    path('vetzone-orders-Cancelled/', VzOrdersCancelledView.as_view(), name='orders-Cancelled'),#
    path('order-details-cancelled/<int:order_id>/', OrderDetailCancelledView.as_view(), name='order-detail-Cancelled'),
    path('Admin_register/', RegistrationView.as_view(), name='register'),
    # path('Admin_login/', LoginView.as_view(), name='login'),
    path('Active-vetzone-list/', ActiveVetzoneListView.as_view(), name='Active-vetzone-list'),
    path('Active-vetzone-DetailView/<int:vetzone_id>/', VetzoneActiveDetailView.as_view(), name='Active-vetzone-DetailView'),
    path('Closed-vetzone-list/', ClosedVetzoneListView.as_view(), name='Closed-vetzone-list'),
    path('Closed-vetzone-DetailView/<int:vetzone_id>/', VetzoneClosedDetailView.as_view(), name='Closed-vetzone-DetailView'),
    path('vetzone-close-requests/', VetzoneRemarkUpdateView.as_view(), name='vetzone-close-requests'),
    path('vetzone-Inventory/<int:vetzone_id>/', VetZoneProductAvailabilityView.as_view(), name='vetzone-Inventory'),

    path('delivery-challan/report/', DeliveryChallanReportView.as_view(), name='delivery_challan_report'),

    path('Dashboard-new/', OrderAndProductDetailsView.as_view(), name='Dashboard-new'),
    path('Vetzone-Drop-Down/', VetZoneDropDownView.as_view(), name='Vetzone-Drop-Down'),
    path('VetZone-Wise-Quantity-Wise-Stock-Report/', DisplayReportView.as_view(), name='VetZone-Wise-Quantit-Wise-Stock-Report'),
    path('VetZone-Wise-Amount-Wise-Stock-Report/', DisplayReportAmountView.as_view(), name='VetZone-Wise-Amount-Wise-Stock-Report'),
    path('VetZone-Wise-Amount-Wise-Stock-Report/', VzQuantityandAmountView.as_view(), name='VetZone-Wise-Amount-Wise-Stock-Report'),
    path('Finance-customers-approval-list/', CustomerApprovalListView.as_view(), name='customers-approval-list'),
    path('Finance-Customer-Approval-Detail/<int:customer_id>/', CustomerApprovalDetailView.as_view(), name='customers-approval-detail'),
    path('Ceo_customers_approval_list/', CeoCustomerApprovalListView.as_view(), name='ceo_customers_approval_list'),
    path('Ceo_customers_approval_detail/<int:customer_id>/', CeoCustomerApprovalDetailView.as_view(), name='Ceo_customers_approval_detail'),
    path('Admin_customers_approval_list/', AdminCustomerApprovalListView.as_view(), name='Admin_customers_approval_list'), 
    path('Admin_customers_approval_detail/<int:customer_id>/', AdminCustomerApprovalDetailView.as_view(), name='Admin_customers_approval_detail'),
    path('Headquarters_DropDown/', HeadquartersDropDownListView.as_view(), name='Headquarters_DropDown'),  
    path('Divisions_DropDown/', DivisionDropDownListView.as_view(), name='Divisions_DropDown'),  
    path('suppliers_dropdown/', SuppliersDropdownView.as_view(), name='suppliers_dropdown'),
    path('customer_roles/', CustomerRoleDropdownView.as_view(), name='customer_roles_dropdown'),
    path('states_dropdown/', StateDropdownView.as_view(), name='state_dropdown'),
    path('distributor_types_dropdown/', DistributorTypeDropdownView.as_view(), name='distributor_type_dropdown'),
    path('customer_registration/', CustomerRegistrationnewView.as_view(), name='customer_registration'),
    path('customer_login/', CustomerLoginView.as_view(), name='customer_login'),
    path('Active_customer_list/', ActiveCustomerListView.as_view(), name='Active_customer_list'),
    path('Active_customer_list_Detail/<int:customer_id>/', ActiveCustomerDetailView.as_view(), name='Active_customer_list_Detail'),
    path('ComPendingCustomerOrderListView/', ComPendingCustomerOrderListView.as_view(), name='ComPendingCustomerOrderListView'),
    path('COM_CustomerOrders_pending/<int:order_id>/', PendingPlacedOrderDetailsView.as_view(), name='COM_CustomerOrders_pending'),  
    path('COE_CustomerOnlineOrdersInprocess/', CoeCustomerOnlineOrdersInprocessListView.as_view(), name='COE_CustomerOnlineOrdersInprocess_list'),
    path('COE_CustomerOnlineOrdersDispatched/', CoeCustomerOnlineOrdersDispatchedListView.as_view(), name='COE_CustomerOnlineOrdersDispatched_list'),
    path('CreaditPaymentOrdersDispatched/', CreditPaymentOrders_DispatchedListView.as_view(), name='COE_CustomerOnlineOrdersDispatched_list'),
    path('Customer_invoice/<int:order_id>/', CustomerinvoiceView.as_view(), name='Customer_invoice'),
    path('batch/<int:product_id>/', BatchDropdownAPIView.as_view(), name='batch-dropdown'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
    path('candf_dropdown/', CandFDropdownView.as_view(), name='candf_dropdown'),
    path('customer/login/', CustomerauthLoginView.as_view(), name='customer_login'),
    # 
    path('get-products-by-division/', ProductsByDivision.as_view(), name='get-products-by-division'),
    path('get-products-details/', ProductDetails.as_view(), name='get-products-details'),
    path('calculate-margin/', CalculateLotDetails.as_view(), name='calculate-margin'),
    path('placeorder/', PlaceOrder.as_view(), name='placeorder'),
    path('addto-cart/', AddToCart.as_view(), name='addto-cart'),

    # 
    path('Get_Batch_allocated/<int:order_id>/', ComBatchAllocatedDetailsView.as_view(), name='Get_Batch_allocated'),  
    path('Com_BatchAllocated_disc_allocate/<int:order_id>/', ComBatchAllocatedInvoiceView.as_view(), name='Com_BatchAllocated_disc_allocate'),    
    path('COM_CustomerOrders_INPROCESS_List/', COMCustomerOrderListInprocessView.as_view(), name='COM_CustomerOrders_INPROCESS_List'),
    path('COM_CustomerOrders_DISPATCH_List/', COMCustomerOrderListDispatchView.as_view(), name='COM_CustomerOrders_DISPATCH_List'),



]

# # Adding media file handling during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

