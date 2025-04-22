
from django.contrib import admin
from django.urls import path
from api.views import UserRegistrationView,UserLoginView
from api.views import UserProfileView,UserChangePasswordView, SendPasswordResetEmailView
from api.views import UserResetPasswordView
from api.views import UserListView
from .views import CreatePostView
from .views import FetchUserPostListView, UserPostsView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-rest-password-email/', SendPasswordResetEmailView.as_view(), name='password-reset'),
    path('reset-password/<uid>/<token>/', UserResetPasswordView.as_view(), name='password-reset-confirm'),
    path('all-users/', UserListView.as_view(), name='user-list'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('fetch-all-posts/', FetchUserPostListView.as_view(), name='fetch-all-posts'),
    path('user-posts/<str:user_id>/', UserPostsView.as_view(), name='user-specific-posts'),
 
    
    

]
