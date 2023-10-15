from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Photo, Comment, Like
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse,HttpResponseForbidden
from django.urls import reverse
from django.http import FileResponse
from django.core.paginator import Paginator
from django_user_agents.utils import get_user_agent
from allauth.socialaccount.views import SignupView
from .forms import MyCustomSocialSignupForm, RegistrationForm
import re
from django.contrib.auth import get_user_model
from verify_email import send_verification_email
from django.template import RequestContext
User = get_user_model()


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            return render(request, "photos/login.html", {"problem": "Account not registered"})
        if not user.is_active:
            return render(request, "photos/email_confirmation.html")
    
        user = authenticate(request, username=username, password=password) 
       
        if user is not None:
            login(request, user)
            return redirect("gallery")
        else:
            return render(request, "photos/login.html", {"problem": "Incorrect Username or Password!"})

    return render(request, "photos/login.html") 


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("gallery")
 

def registerUser(request):
    form = RegistrationForm()
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
           
            email = form.cleaned_data["email"]
            confirmPassword = form.cleaned_data["confirmpassword"]


            pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

            if not re.match(r"^[a-zA-Z][a-zA-Z0-9._]{3,11}$", username):
                return render(
                    request,
                    "photos/register_form.html",
                    {
                        "form": form,
                        "error": "Username must start with a letter, should be 4 to 12 characters long, and can contain letters, numbers, periods, and underscores."
                    },
                )

            if re.fullmatch(pattern, email) == None:
                return render(
                    request,
                    "photos/register_form.html",
                    {
                        "form": form,
                        "error": "Not a valid email address"},
                )

            if len(username) < 3:
                return render(
                    request,
                    "photos/register_form.html",
                    {
                        "form": form,
                        "error": "Username must be at least 3 characters long"},
                )

            if len(password) < 8:
                return render(
                    request,
                    "photos/register_form.html",
                    {"form": form,"error": "Password must be at least 8 characters long"},
                )

            if User.objects.filter(username=username).exists():
                return render(
                    request,
                    "photos/register_form.html",
                    {"form": form,"error": "Username is already taken"},
                )
            if User.objects.filter(email=email).exists():
                return render(
                    request,
                    "photos/register_form.html",
                    {"form": form,"error": "Email is already in use"},
                )

            if password == confirmPassword:
                try:
                    inactive_user = form.save(commit=False)
                    inactive_user.set_password(form.cleaned_data['password'])
                    inactive_user = send_verification_email(request, form)
                    
                    return render(request, 'photos/email_confirmation.html')
                except:
                    return render(
                    request,
                    "photos/register_form.html",
                    {"form": form,"error": "Something went wrong!"},
                )
                    
            else:
                return render(
                    request,
                    "photos/register_form.html",
                    {"error": "Password and confirm password doesn't match "},
                )
            
    return render(request, "photos/register_form.html", {"form": form})


class CustomSignupView(SignupView):
    template_name = "socialaccount/signup.html"
    form_class = MyCustomSocialSignupForm


def global_view(request):
    searchTerm = request.GET.get("searchImage")

    if searchTerm:
        photos = Photo.objects.filter(
            Q(publicAccess=True)
            & (
                Q(category__name__icontains=searchTerm)
                | Q(description__icontains=searchTerm)
                | Q(user__username__icontains=searchTerm)
            )
        ).order_by("-upload_datetime")
    else:
        photos = Photo.objects.filter(publicAccess=True).order_by("-upload_datetime")

    paginator = Paginator(photos, 24)
    page = int(request.GET.get("page", 1))
    try:
        photos = paginator.page(page)
    except:
        return HttpResponse("<h3 class='text-center'> No more Photos</h3>")

    context = {"photos": photos, "searchTerm": searchTerm, "page": page}

    if request.htmx:
        return render(request, "photos/loop_global.html", context=context)
    else:
        return render(request, "photos/global.html", context=context)


@login_required(login_url="login")
def gallery(request):
    user = request.user
    category = request.GET.get("category")
    searchTerm = request.GET.get("searchImage")
    categories = Category.objects.filter(user=user)
    if searchTerm:
        photos = Photo.objects.filter(
            Q(user=user)
            & (
                Q(category__name__icontains=searchTerm)
                | Q(description__icontains=searchTerm)
            )
        )
    else:
        if category == None:
            photos = Photo.objects.filter(user=user)
        else:
            photos = Photo.objects.filter(
                Q(category__name__contains=category) & Q(user=user)
            )

    paginator = Paginator(photos, 24)
    page = int(request.GET.get("page", 1))
    try:
        photos = paginator.page(page)
    except:
        return HttpResponse("<h3 class='text-center'> No more Photos</h3>")
    
    context = {'category':category,"categories": categories,"photos": photos, "searchTerm": searchTerm, "page": page}
    
    if request.htmx:
        return render(request,"photos/loop_gallery.html",context=context)
    return render(request, "photos/gallery.html", context=context)


@login_required(login_url="login")
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    comments = Comment.objects.filter(photo=photo)
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        print(user_agent)
        return render(
            request, "photos/mobile_photo.html", {"photo": photo, "comments": comments}
        )
    else:
        return render(
            request, "photos/photo.html", {"photo": photo, "comments": comments}
        )


@login_required(login_url="login")
def editPage(request, pk):
    user = request.user
    categories = Category.objects.filter(user=user)

    if request.method == "GET":
        try:
            photo = Photo.objects.get(id=pk, user=user)
        except Photo.DoesNotExist:
            return render(request, "gallery.html", {"message": "Photo not found."})
    if request.method == "POST":
        data = request.POST

        if data["category"] != "none":
            category = Category.objects.get(user=user, id=data["category"])
        elif data["category_new"] != "":
            category, created = Category.objects.get_or_create(
                user=user, name=data["category_new"]
            )
        else:
            category = None

        publicOrNot = False

        if data["global_access"] == "public":
            publicOrNot = True

        photo = get_object_or_404(Photo, pk=pk, user=request.user)
        photo.category = category
        photo.description = data["description"]
        photo.publicAccess = publicOrNot
        photo.save()
        return redirect("gallery")

    return render(
        request, "photos/edit.html", {"photo": photo, "categories": categories}
    )


@login_required(login_url="login")
def addPhoto(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist("images")
        valid_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'webp', 'svg', 'tiff', 'tif', 'gif', 'heif']
        
        if len(images) > 5:
            return render(request, "photos/add.html", {"error": "Currently, Atmost 5 images upload supported."})

        if data["category"] != "none":
            category = Category.objects.get(user=user, id=data["category"])
        elif data["category_new"] != "":
            category, created = Category.objects.get_or_create(
                user=user, name=data["category_new"]
            )
        else:
            category = None

        publicOrNot = False

        if data["global_access"] == "public":
            publicOrNot = True

        for image in images:
            if not any(image.name.endswith(ext) for ext in valid_extensions):
                return render(request, "photos/add.html", {"error": "Please enter valid image file!"})
            
            photo = Photo.objects.create(
                user=user,
                category=category,
                description=data["description"],
                image=image,
                publicAccess=publicOrNot,
            )
        return redirect("gallery")

    return render(request, "photos/add.html", {"categories": categories})




@login_required(login_url="login")
def delete_category_and_images(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    user = request.user
    if category.user != user:
        return HttpResponseForbidden("You do not have permission to delete")

    photos_to_delete = Photo.objects.filter(Q(category=category) & Q(user=user))

    category.delete()

    # Delete all associated photos.
    for photo in photos_to_delete:
        photo.delete()

    # Redirect to a specific page after the deletion is complete.
    return redirect(
        "gallery"
    )  


@login_required(login_url="login")
def delete_images(request):
    # Get the list of selected photo IDs from the query parameters
    photo_ids = request.GET.getlist("photo_ids")
    # Get the list of photos to be deleted
    photo_ids = photo_ids[0].split(",")

    for photo_id in photo_ids:
        photo = Photo.objects.filter(pk=photo_id)
        photo.delete()

    # Delete the photos from the database

    # Return a success response
    return JsonResponse({"success": True})


@login_required(login_url="login")
def like_photo(request, pk):
    if request.method == "POST":
        photo = Photo.objects.get(pk=pk)
        if request.user in photo.likes.all():
            photo.likes.remove(request.user)
        else:
            photo.likes.add(request.user)

        return redirect(reverse("photo", args=[str(pk)]))


@login_required(login_url="login")
def comment_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    if request.method == "POST":
        text = request.POST.get("text")
        Comment.objects.create(user=request.user, photo=photo, text=text)
    return redirect(reverse("photo", args=[str(pk)]))


from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Photo


@login_required(login_url="login")
def download(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    image_path = photo.image.path
    response = FileResponse(open(image_path, "rb"))
    response["Content-Disposition"] = f'attachment; filename="{photo.image.name}"'
    return response

@login_required(login_url="login")
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user == request.user:
        comment.delete()
        previous_page = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_page)  
    else:
        return HttpResponse(status=403) 
    
    
    

def page_not_found(request,exception=None):
    context = {}
    response = render(request, "/404.html", context=context)
    response.status_code = 404
    return response