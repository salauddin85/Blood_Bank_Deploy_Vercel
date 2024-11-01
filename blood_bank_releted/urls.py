from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AboutUsViewSet, ContactViewSet,  
    FeedbackViewSet,BlogPostViewSet,All_Feddback,
    SubscriptionViewSet,SSLCommerzPaymentView,
    SSLCommerzPaymentSuccessView,SSLCommerzPaymentFailView
)
# BlogPostViewSet,

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'about-us', AboutUsViewSet, basename='about-us')
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'blog', BlogPostViewSet, basename='blog')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'all_feedback', All_Feddback, basename='all_feedback')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
# router.register('payment_details',PaymentDetailsView, basename='paymentdetails')


urlpatterns = [
    path('', include(router.urls)),
    path('payment/initiate/', SSLCommerzPaymentView.as_view(), name='payment_initiate'),
    path('payment/success/<str:tran_id>/<int:user_id>/', SSLCommerzPaymentSuccessView.as_view(), name='payment_success'),
    path('payment/fail/<str:tran_id>/<int:user_id>/', SSLCommerzPaymentFailView.as_view(), name='payment_fail'),
]
