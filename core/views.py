from django.shortcuts import render, redirect
from datetime import date
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import Xuser
from django.contrib.auth import get_user_model


# Create your views here.
def landing_page(request):
    return render(request, "core/landing_page.html")
def signup_view(request):
    msg = ""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # validating  the date feilds
        day_raw = request.POST.get("db_day")
        month_raw = request.POST.get("db_month")
        year_raw = request.POST.get("db_year")
        if not day_raw or not month_raw or not year_raw:
            msg = "Please select your full birth date"
            return render(request,"core/signup.html",context = {"error":msg})
        
        try:
            day = int(request.POST.get("db_day"))
            month = int(request.POST.get("db_month"))
            year = int(request.POST.get("db_year"))
            dob = date(year, month, day)
        except(TypeError,ValueError):
            msg = "Invalid birth date. Please select a valid day, month, and year."
            return render(request,"core/signup.html",context = {"error":msg})
        

        # VALIDATING THE USER AND CHECKING DUPLICATES USER DETAILS
        if Xuser.objects.filter(username=username).exists():
            msg = "Username already take . Please choose another ."
            return render(request, "core/signup.html",context={"error":msg})
        if Xuser.objects.filter(email=email).exists():
            msg = "Email already registered. Try logging in or use another."
            return render(request,"core/signup.html",context={"error":msg})

        user = Xuser(username=username, email=email, dob=dob, is_active=False)
        user.set_password(password)
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verification_link = request.build_absolute_uri(
            reverse("verify_email", kwargs={"uidb64": uid, "token": token})
        )
        send_mail(
            subject="Verify your mail",
            message=f"Click the link to verify your email : {verification_link}",
            from_email="noreplay@xclone.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return render(request, "core/email_sent.html")

    return render(request, "core/signup.html", context={"error": msg})


def signin_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user=user)
                return HttpResponse("home")
            else:
                error = "Please verify your email before logging in ."

        else:
            error = "Invalid Username or password ."

    return render(request, "core/signin.html", context={"error": error})


def verify_email_view(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request,"core/email_verified.html")
    else:
        return HttpResponse("Invalid or expired email link .")
