from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AboutUs, Contact, Feedback,DonorBlogPost,Subscription,Payment
from .serializers import AboutUsSerializer, ContactSerializer, FeedbackSerializer,BlogPostSerializer,SubscriptionSerializer,PaymentSerializer
from events.models import DonationHistory,DonationEvent
from rest_framework.response import Response
from rest_framework import viewsets, status
from .constraints import OFFENSIVE_WORDS
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from events.views import  DonationEventPagination
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import requests
from rest_framework.views import APIView
from django.conf import settings
import random, string
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from requests.exceptions import ConnectTimeout
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.http import JsonResponse
# from accounts.permissions import IsAdmin
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework.decorators import action






# class PaymentDetailsView(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Payment.objects.filter(status="Completed")
#         return Payment.objects.filter(user=self.request.user)


def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



Amount = ""
class SSLCommerzPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        global Amount
        amount = request.data.get('amount')
        address = request.data.get('address')

        
        Amount = amount

        # Creating a Payment instance
        payment = Payment.objects.create(
            user=request.user,
            amount=amount
        )
        # print(payment.id, "177 number line")

        # POST request to SSLCommerz API
        tran_id = unique_transaction_id_generator()
        
        # POST request to SSLCommerz API
        sslcommerz_data = {
            'store_id': 'cilda671e59f35de90',
            'store_passwd': 'cilda671e59f35de90@ssl',
            'total_amount': amount,
            'currency': 'BDT',
            'tran_id': tran_id,  # Transaction ID is placed here
            'success_url': f"https://blood-bank-deploy-vercel.vercel.app/blood_bank_releted/payment/success/{tran_id}/{request.user.id}/",
            'fail_url': f"https://blood-bank-deploy-vercel.vercel.app/blood_bank_releted/payment/fail/{tran_id}/{request.user.id}/",
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_add1': address['address_line_1'],
            'cus_add2': address['address_line_2'],  # Address line 2
            'cus_city': address['city'],  # City added here
            'cus_phone': address['phoneNumber'],
            'cus_country': address['country'],  # Country added here
            'shipping_method': 'NO',
            'product_name': 'Donation',
            'product_category': 'Dontion amount',
            'product_profile': 'general',
        }
        try:
            response = requests.post('https://sandbox.sslcommerz.com/gwprocess/v4/api.php', data=sslcommerz_data, timeout=10)
            payment_data = response.json()

        except ConnectTimeout:
            return Response({'error': 'Connection to payment gateway timed out. Please try again later.'}, status=503)

        if payment_data.get('status') == 'SUCCESS':
            payment.transaction_id = tran_id  # Use a default value if tran_id is missing
            print(payment.transaction_id, "transaction id ")
            payment.save()
            return Response({'status': 'success', 'user_id': request.user.id, 'transaction_id': tran_id, 'redirect_url': payment_data['GatewayPageURL']})

        else:
            return Response({'status': 'failed', 'message': payment_data.get('failedreason', 'SSLCommerz payment failed')})


class SSLCommerzPaymentSuccessView(APIView):
    
    def post(self, request, user_id, tran_id):
        # Finding the correct user with `user_id`
        user = get_object_or_404(User, id=user_id)
        payment = get_object_or_404(Payment, transaction_id=tran_id)

        # Checking and updating payment status
        payment.status = 'Completed'
        payment.save()

        # Finding products for purchase
        
        
        # print(f"Total amount is {Amount}")
        # Email Confirmation
        # email_subject = "Donation Confirmation"
        # email_body = render_to_string("cartpurchase_email.html", {
        #     'user': user,
        #     'payment_status': payment.status,
        #     'transaction_id': payment.transaction_id,
        #     'amount': Amount  # Amount must be defined beforehand
        # })
        # email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        # email.attach_alternative(email_body, 'text/html')
        # email.send()

        response_data = {
            'status': 'success',
            'transaction_id': payment.transaction_id,
            'amount': payment.amount,
            
        }

        query_string = urlencode(response_data)
        return redirect(f"https://salauddin85.github.io/Blood_Bank_Frontend/payment_Success.html?{query_string}")
        


class SSLCommerzPaymentFailView(APIView):
    def post(self, request, user_id, tran_id):

        # Fetch payment, update status if exists
        payment = get_object_or_404(Payment, transaction_id=tran_id)
        payment.status = 'Failed'
        payment.save()
        response_data = {
            'status': 'failed',
            'amount': payment.amount,
        }

        query_string = urlencode(response_data)
        return redirect(f"https://salauddin85.github.io/Blood_Bank_Frontend/payment_fail.html?{query_string}")




class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_object(self):
        # Return the first About Us record
        return AboutUs.objects.first()


class ContactViewSet(viewsets.ModelViewSet):
    
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
   # Only allow POST requests


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = DonorBlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = DonationEventPagination

    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        image_url = serializer.validated_data.get('image')
        
        if not image_url:
            raise ValidationError({"detail":"Image url not found "})
        # Check if title and content are empty
        if not title or not content:
            raise ValidationError({"detail": "Title and content must be provided."})

        # ব্লগ পোস্ট তৈরি করুন এবং সেভ করুন
        serializer.save(author=user, image=image_url)  # লোকালি ইমেজ সেভ হবে

        return Response(
            {"detail": "Blog post created successfully!"},
            status=status.HTTP_201_CREATED
        )



class FeedbackViewSet(viewsets.ModelViewSet):
    # queryset = Feedback.objects.all()

    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Only return feedbacks for the logged-in user
        user = self.request.user
        if user.is_authenticated:
            return Feedback.objects.filter(donor=user)
        return Feedback.objects.none()  # Return empty queryset for unauthenticated users

    def perform_create(self, serializer):
        user = self.request.user
        print(user, "Logged in user")

        # Check if feedback already exists for this donor
        if Feedback.objects.filter(donor=user).exists():
            print("Feedback already exists for this donor")
            raise ValidationError("Your feedback already exists")

        # Check if the user has donation history before creating feedback
        if DonationHistory.objects.filter(user=user).exists():
            serializer.save(donor=user)
            return Response({"detail": "Thank you! Your feedback has been submitted successfully."}, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError("We could not find your donation history. You must have a recorded donation in order to submit feedback.")



class All_Feddback(viewsets.ModelViewSet):
    queryset=Feedback.objects.all()
    serializer_class=FeedbackSerializer
    pagination_class=DonationEventPagination

    @action(detail=False,methods=['get'])
    def all_feedback(self,request):
        feedback=Feedback.objects.all()
        serializer=FeedbackSerializer(feedback,many=True)
        return Response({'all_feedback':serializer.data})


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        # Directly create subscription for the logged-in user
        subscription = Subscription.objects.filter(user=user).exists()
        if subscription:
            raise ValidationError({"detail": "Your subscription already exists"})  # Modified to a dictionary for better frontend handling
        
        # Validate serializer
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        # Save subscription
        serializer.save(user=self.request.user)
        return Response({"detail": "Thank you! for Subscription us"}, status=status.HTTP_201_CREATED)


