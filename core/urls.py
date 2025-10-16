from django.urls import path
from . import views
urlpatterns = [
    path("",views.landing_page,name="landing"),
    path("signup/",views.signup_view,name="signup"),
    path("signin/",views.signin_view,name="signin"),
    path("verify-email/<uidb64>/<token>",views.verify_email_view,name="verify_email"),
    path("profile/complete/",views.profile_completion_view,name="profile_completion"),
    path("home/",views.home_page_view,name="home_page"),
    path("follow/<str:username>",views.follow_user_view,name="follow_user"),
    path("settings/profile",views.profile_edit_view,name="profile_edit"),
    path("logout/",views.logout_view,name="logout")
]