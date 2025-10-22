from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            avatar = form.cleaned_data.get("avatar")
            if avatar:
                user.profile.avatar = avatar
                user.profile.save()
            login(request, user)
            return redirect("lista_productos")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        if "avatar" in request.FILES:
            user.profile.avatar = request.FILES["avatar"]
        user.save()
        user.profile.save()
        return redirect("profile")
    return render(request, "accounts/profile.html")