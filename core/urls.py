from django.urls import path
from . import views
urlpatterns = [
    path("",views.landing_page,name="landing"),
    path("signup/",views.signup_view,name="signup"),
    path("signin/",views.signin_view,name="signin"),
    path("verify-email/<uidb64>/<token>",views.verify_email_view,name="verify_email")

]