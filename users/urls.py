from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('resend_verification_code/', views.ResendVerificationCode.as_view()),
    path('verify_email/', views.SignupVerificationView.as_view()),
    path('my_profile/', views.MyProfileView.as_view()),
    path('my_profile_picture/', views.ProfilePictureView.as_view()),
    path('reset_password/', views.ResetPasswordView.as_view()),
]