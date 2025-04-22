from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.serializers import UserRegistrationSerializer, UserLoginSerializer,UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer
from api.serializers import UserPasswordResetSeriazlier
from django.contrib.auth import authenticate
from api.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from .models import Post 
from api.models import User
from rest_framework.permissions import IsAuthenticated  
from rest_framework.generics import ListAPIView
from .serializers import PostSerializer

# fetch all the user data
class UserListView(ListAPIView):
    """
    View to list all users.
    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated] 
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if(serializer.is_valid()):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successfull'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        
        serializer = UserLoginSerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Successfull'},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{"non_field_errors":['Email or Password is invalid']}},status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        print("Request Headers....:", request.headers)
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
   
# class SendPasswordResetEmailView(APIView):
#     renderer_classes = [UserRenderer]
#     def post(self, request, format=None):
#         serializer = SendPasswordResetEmailSeriazlier(data=request.data)
#         if(serializer.is_valid(raise_exception=True)):
#             return Response({'msg':'Password Reset link has been send,Please check your Email'}, 
#                             status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class UserResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSeriazlier(data=request.data,
        context=({'uid':uid, 'token':token}))
        if(serializer.is_valid(raise_exception=True)):
            return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ////////////////// Posts ////////////////////////////////////////////////////////////////////////////////////////
class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Automatically link to authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# fetch all the user data
class FetchUserPostListView(ListAPIView):
    """
    View to list all posts from all users.
    Requires authentication.
    """
    queryset = Post.objects.all().order_by('-created_at')  # You can order them by latest
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
class UserPostsView(ListAPIView):
    """
    View to list all posts from a specific user.
    Requires authentication.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        # Verify user exists
        get_object_or_404(User, id=user_id)
        return Post.objects.filter(user_id=user_id).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)