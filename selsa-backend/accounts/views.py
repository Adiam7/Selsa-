from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from . import serializers, services
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.create_user(serializer.validated_data)
        return Response({'message': 'Check your email to verify account.'}, status=201)

class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            services.verify_user_email(token)
            return Response({'message': 'Email verified'})
        except ValueError:
            return Response({'error': 'Invalid token'}, status=400)

class LoginView(APIView):

    def get(self, request):
        return Response({"detail": "Login view endpoint. Please POST your credentials."})
    
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Create JWT tokens
        refresh = RefreshToken.for_user(user)

        # Return user info + tokens
        if not user.is_email_verified:
            return Response({'error': 'Email not verified'}, status=status.HTTP_403_FORBIDDEN)
        # If the user is not active, return an error
        if not user.is_active:  
            return Response({'error': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)
        # If the user is active, proceed with login
        # Create JWT tokens
        # Return user info + tokens
        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "isEmailVerified": user.is_email_verified,
            },
            "accessToken": str(refresh.access_token),
            "refreshToken": str(refresh),
        }, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Wrong old password'}, status=400)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed'})

class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = serializers.ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.initiate_password_reset(serializer.validated_data['email'])
        return Response({'message': 'Password reset email sent'})

class ResetPasswordConfirmView(APIView):
    def post(self, request):
        serializer = serializers.ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.confirm_password_reset(
                serializer.validated_data['token'],
                serializer.validated_data['new_password']
            )
            return Response({'message': 'Password reset successful'})
        except ValueError:
            return Response({'error': 'Invalid token'}, status=400)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        serializer = serializers.UserProfileUpdateSerializer(
            instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)    
    
class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = serializers.UserListSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.create_user(serializer.validated_data)
        return Response({'message': 'User created successfully'}, status=201)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = services.get_user_by_id(user_id)
        if not user:
            return Response({'error': 'User not found'}, status=404)
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = services.get_user_by_id(user_id)
        if not user:
            return Response({'error': 'User not found'}, status=404)
        serializer = serializers.UserUpdateSerializer(
            instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, user_id):
        user = services.get_user_by_id(user_id)
        if not user:
            return Response({'error': 'User not found'}, status=404)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=204)
    
class forgetPasswordView(APIView):
    def post(self, request):
        serializer = serializers.ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.send_reset_password_email(serializer.validated_data['email'])
        return Response({'message': 'Reset password email sent'}, status=200)