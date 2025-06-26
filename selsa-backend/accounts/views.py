# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_backends
from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


@login_required  # Ensures only logged-in users can access the dashboard
def dashboard_view(request):
    return render(request, "registration/dashboard.html")  # Render a dashboard template

"""
       if user.is_staff:  # If the user is an admin/staff
                return redirect("admin_dashboard")
            else:  # Regular users
                return redirect("user_dashboard")
"""

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
           # login(request, user)
           # return redirect("/registration/login")
        
        # Automatically assign the first backend
            backend = get_backends()[0]  # Select the first available backend
            login(request, user, backend=backend.__class__.__module__ + "." + backend.__class__.__name__)
            
        #return redirect("dashboard")
            #return redirect("dashboard")
        return render(request, "registration/dashboard.html")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def home_view(request):
    return render(request,"pages/index.html")


#  login view in your views.py
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Make sure this matches your template path

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect users after login (update as needed)

def profile(request):
    return render(request, 'registration/profile.html')

