from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth import logout
from photos.models import Photo
from django.template import RequestContext
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


User = get_user_model()




@login_required(login_url="login/")
def edit_profile(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        print(request.POST.get("bio"))
        fullname = request.POST.get("puraname")
        if request.FILES.get('pfp') is not None:
            user.pfp = request.FILES.get("pfp")
        user.user_bio = request.POST.get("bio")
        if len(user.user_bio) > 500:
            error_message = "Bio cannot be more than 500 characters."
            return render(request, "users/edit_profile.html", {"error_message": error_message})
        if len(fullname) > 25:
            error_message = "Name cannot be more than 25 characters."
            return render(request, "users/edit_profile.html", {"error_message": error_message})
        
        full_name_parts = fullname.split()
        user.first_name = full_name_parts[0] if full_name_parts else ""
        user.last_name = full_name_parts[1] if len(full_name_parts) > 1 else ""
        user.save()
        return redirect("gallery")
    return render(request, "users/edit_profile.html")


@login_required(login_url="login/")
def view_profile(request, username=None):
    if username:
        try:
            user = get_object_or_404(User, username=username)
        except:
            return render(
                request, "users/view_profile.html", {"error": "No username found"}
            )
    else:
        user = request.user

    content_type = request.GET.get("filter", "")

    if content_type == "" or content_type == 'global-posts':
        photos = Photo.objects.filter(Q(user=user) & Q(publicAccess=True))
    elif content_type == "commented-posts":
        photos = Photo.objects.filter(Q(comments=user))
    elif  content_type == "liked-posts":
        photos = Photo.objects.filter(Q(likes=user))
    elif content_type == "private-posts":
        photos = Photo.objects.filter(Q(user=user) & Q(publicAccess=False))

    context = {"profile": user, "photos": photos , "error":None}

    return render(request, "users/view_profile.html", context=context)


@login_required(login_url="login/")
def profile_delete(request):
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        logout(request)
        user.delete()
        messages.success(request, "Account deleted, What a pity")
        return redirect("/")

    return render(request, "users/profile_delete.html")



# HTTP Error 400
def page_not_found(request,exception=None):
    context = {}
    response = render(request, "/404.html", context=context)
    response.status_code = 404
    return response