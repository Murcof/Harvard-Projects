import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .util import NewPostForm
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, UserFollowing
from django.core.paginator import Paginator
from django.core import serializers



def index(request, page_number=1):
    if request.method == "GET":
        if User.is_authenticated:
            posts_list = Post.objects.all().order_by("-timestamp")
            paginator = Paginator(posts_list, 10)  # show 10 posts per page
            page_object = paginator.get_page(page_number)
            return render(request, "network/index.html", {
                'new_post_form': NewPostForm(),
                'page_object': page_object,
                'page_number': page_number
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        pass

def profile (request,user_id,page_number=1):
    if request.method == "GET":
        profile_user = User.objects.get(id=user_id)

        posts_list = Post.objects.filter(creator=profile_user).order_by("-timestamp")
        paginator = Paginator(posts_list, 10)  # show 10 posts per page
        page_object = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            'page_object': page_object,
            'page_number': page_number,
            'profile_user': profile_user,
            'following': profile_user.following.all(),
            'followers': profile_user.followers.all().values_list('user_id', flat=True),
        })
    else:
        pass
@csrf_exempt
def follow(request, profile_user_id):
    user = User.objects.get(pk=request.user.id)
    following_user = User.objects.get(pk=profile_user_id)
    user_following = UserFollowing(user_id=user, following_user_id=following_user)
    user_following.save()
    return JsonResponse({"message": "User Followed"}, status=200)

@csrf_exempt
def unfollow(request, profile_user_id):
    user = User.objects.get(pk=request.user.id)
    following_user = User.objects.get(pk=profile_user_id)
    user_following = UserFollowing.objects.filter(user_id=user).filter(following_user_id=following_user)
    user_following.delete()
    return JsonResponse({"message": "User Unfollowed"}, status=200)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        files = request.FILES
        photo = files['photo']

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, photo = photo)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def newpost(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        form = NewPostForm(json.loads(request.body))
        if form.is_valid():
            data = json.loads(request.body)
            content = data.get("content", "")
            timestamp = timezone.now()
            post = Post(creator=request.user, content=content, timestamp=timestamp)
            post.save()

            user = User.objects.get(pk=request.user.id)
            photo_url = user.photo

            return JsonResponse({"message": "New post sent successfully.",
                                 'photo_url': f"{photo_url}",
                                 'post_id': f"{post.id}",
                                 'user': f"{user}"}, status=201)
        else:
            return JsonResponse({"error": "Unable to create your post."}, status=400)

@csrf_exempt
def like_post(request, post_id): #Although its name, this function is used to like or unlike posts.

    # like/unlike must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        user = User.objects.get(username=request.user)
        post = Post.objects.get(pk=post_id)
        post_likers = post.likers.all()
        if user in post_likers:
            post.likers.remove(user)
            return JsonResponse({"message": f"Post Unliked"}, status=201)
        else:
            post.likers.add(user)
            return JsonResponse({"message": f"Post Liked"}, status=201)

@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(username=request.user)
        if post.creator != user:
            return JsonResponse({"error": "Only the creator can edit the post."}, status=400)
        else:
            data = json.loads(request.body)
            content = data.get("content","")
            post.content = content
            post.edited = True
            post.save()
            return JsonResponse({"message": "Post updated."}, status=200)

def following(request,page_number=1):
    following = request.user.following.all().values('following_user_id_id')
    posts_list = Post.objects.filter(creator__in=following).order_by("-timestamp")

    paginator = Paginator(posts_list, 10)  # show 10 posts per page
    page_object = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        'new_post_form': NewPostForm(),
        'page_object': page_object,
        'page_number': page_number
    })