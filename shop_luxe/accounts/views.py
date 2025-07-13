from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_data = UserProfileSerializer(user).data
        return Response({
            "user": user_data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['email'] 
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = UserProfileSerializer(user).data
            return Response({
                "user": user_data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        
        return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email__iexact=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_link = f"https://your-frontend-domain.com/reset-password/{uid}/{token}/"
        
        print(f"Password Reset Link (for testing): {reset_link}")
        
        return Response({"message": "If a user with this email exists, a password reset link will be sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Your password has been changed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "The reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
