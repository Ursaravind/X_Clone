from django.shortcuts import render, redirect,get_object_or_404
from datetime import date
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from .models import Xuser, Tweet
from django.contrib.auth import get_user_model
from decouple import config
from django.contrib.auth.decorators import login_required
from .forms import ProfileCompletionForm, TweetForm,ProfileEditForm


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
            return render(request, "core/signup.html", context={"error": msg})

        try:
            day = int(request.POST.get("db_day"))
            month = int(request.POST.get("db_month"))
            year = int(request.POST.get("db_year"))
            dob = date(year, month, day)
        except (TypeError, ValueError):
            msg = "Invalid birth date. Please select a valid day, month, and year."
            return render(request, "core/signup.html", context={"error": msg})

        # VALIDATING THE USER AND CHECKING DUPLICATES USER DETAILS
        if Xuser.objects.filter(username=username).exists():
            msg = "Username already take . Please choose another ."
            return render(request, "core/signup.html", context={"error": msg})
        if Xuser.objects.filter(email=email).exists():
            msg = "Email already registered. Try logging in or use another."
            return render(request, "core/signup.html", context={"error": msg})

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
            from_email=config("EMAIL_HOST_USER"),
            recipient_list=[email],
            fail_silently=False,
        )
        return render(request, "core/email_sent.html")

    return render(request, "core/signup.html", context={"error": msg})


def signin_view(request):
    error = ""

    if request.method == "POST":
        identifier = request.POST.get("username").strip()
        password = request.POST.get("password")

        user_obj = None
        if "@" in identifier:
            try:
                user_obj = Xuser.objects.get(email__iexact=identifier)
            except:
                error = "Invalid email or password"
        else:
            try:
                user_obj = Xuser.objects.get(username__iexact=identifier)
            except Xuser.DoesNotExist:
                error = "Invalid username or password"
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user=user)
                    if user.is_profile_complete:
                        return redirect("home_page")
                    else:
                        return redirect("profile_completion")
                else:
                    error = "Please verify your email before logging in ."
        else:
            error = "Invalid credentials"

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
        login(request, user)
        return render(request, "core/email_verified.html")
    else:
        return HttpResponse("Invalid or expired email link .")


@login_required
def profile_completion_view(request):
    if request.user.is_profile_complete:
        return redirect("home_page")
    if request.method == "POST":
        form = ProfileCompletionForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_profile_complete = True
            user.save()

            return redirect("signin")
    else:
        form = ProfileCompletionForm(instance=request.user)
    context = {"form": form}

    return render(request, "core/profile_completion.html", context)


@login_required
def home_page_view(request):
    if not request.user.is_profile_complete:
        return redirect("profile_completion")
    form = TweetForm()
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("home_page")

    # Feed Fetching Logic (Posts from followed users)
    # Get the list of IDs of users the current user follows
    followed_users_ids = request.user.following.values_list("id", flat=True)
    # Include the current user's ID so they see their own tweets
    all_target_ids = list(followed_users_ids) + [request.user.id]

    # Fetch tweets from the target users, ordered by newest first (defined in Tweet.Meta)
    feed_tweets = Tweet.objects.filter(user_id__in=all_target_ids).select_related("user")
    # Empty State / Discover Users Logic
    # Simple logic to suggest other users if the feed is empty (and they aren't following anyone)
    suggested_users = None
    if not feed_tweets.exists() and not followed_users_ids:

        # Fetch up to 5 users who are NOT the current user
        suggested_users = Xuser.objects.exclude(id=request.user.id).order_by("?")[:5]

    context = {
        "tweet_form": form,
        "feed_tweets": feed_tweets,
        "suggested_users": suggested_users,
        "user_profile": request.user,  # Current user data for the welcome/sidebar
    }

    # If the user is logged in, they are guaranteed to go to home_page.html
    return render(request, "core/home_page.html", context)


def profile_edit_view(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if request.POST.get('delete_photo'):
                if user.profile_photo:
                    user.profile_photo.delete(save=False)
                user.profile_photo = None
            user.save()
        return redirect("home_page")
    else:
        form = ProfileEditForm(instance=request.user)
        context = {"form":form}
    return render(request,"core/profile_edit.html",context)


def logout_view(request):
    logout(request)
    return redirect("landing")


@login_required
def follow_user_view(request,username):
    target_user = get_object_or_404(Xuser,username=username)
    current_user = request.user

    if current_user == target_user:
        return redirect("home_page")
    if current_user.following.filter(username=username).exists():
        # unfollow logic 
        current_user.following.remove(target_user)
    else:
        # follow logic
        current_user.following.add(target_user)
    return redirect('home_page')


