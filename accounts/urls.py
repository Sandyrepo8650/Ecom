from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register', views.UserRegistrationPageView.as_view(), name='register'),
    path('login', views.UserLoginPageView.as_view(), name='login'),
    path('logout', views.UserLogoutPageView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', views.UserActivatePageView.as_view(), name='activate'),
    path('forgotpassword', views.ForgotPasswordPageView.as_view(), name='forgotpassword'),
    path('resetpassword/<uidb64>/<token>/', views.ResetPasswordPageView.as_view(), name='resetpassword'),
]