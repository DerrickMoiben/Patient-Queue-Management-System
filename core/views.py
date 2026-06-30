from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')




from .forms import UserRegistrationForm


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "User account created successfully.")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {
        "form": form
    }

    return render(request, "register.html", context)





def login_user(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.role == "receptionist":
                return redirect("reception_dashboard")

            elif user.role == "doctor":
                return redirect("doctor_dashboard")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

from django.contrib.auth.decorators import login_required


@login_required
def reception_dashboard(request):
    return render(request, "reception_dashboard.html")


@login_required
def doctor_dashboard(request):
    return render(request, "doctor_dashboard.html")


