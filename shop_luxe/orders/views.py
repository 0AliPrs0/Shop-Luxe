from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    InitiatePaymentSerializer,
)
from .models import Order, Payment
from django.urls import reverse


class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-ordered_at')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

class InitiatePaymentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InitiatePaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data['order_id']
        
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.payment_status not in ['PENDING', 'FAILED']:
            return Response(
                {"error": "Payment cannot be initiated for this order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            gateway='YourPaymentGateway',
            status='PENDING'
        )
        
        base_url = request.build_absolute_uri('/')
        callback_url = base_url + reverse('payment-callback')[1:]
        
        payment_url = (
            f"https://fake-gateway.com/pay"
            f"?amount={payment.amount}"
            f"&payment_id={payment.id}"
            f"&callback_url={callback_url}"
        )
        
        return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)


class PaymentCallbackView(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        payment_id = request.query_params.get('payment_id')
        gateway_status = request.query_params.get('status')
        transaction_id = request.query_params.get('transaction_id')
        
        if not payment_id:
            return Response({"error": "Payment ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        payment = get_object_or_404(Payment, id=payment_id)
        
        if gateway_status == 'success':
            payment.status = 'COMPLETED'
            payment.transaction_id = transaction_id
            payment.save()
            
            order = payment.order
            order.payment_status = 'PAID'
            order.status = 'PROCESSING'
            order.save()
            
            return Response({"message": "Payment successful."}, status=status.HTTP_200_OK)
        
        else:
            payment.status = 'FAILED'
            payment.save()
            
            order = payment.order
            order.payment_status = 'FAILED'
            order.save()
            
            return Response({"error": "Payment failed."}, status=status.HTTP_400_BAD_REQUEST)