from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page_number>", views.index, name="index"),
    path("following/", views.following, name="following"),
    path("following/<int:page_number>", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<int:user_id>/<int:page_number>", views.profile, name="profile"),

    #API Routes
    path("newpost", views.newpost, name="newpost"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("unfollow/<int:profile_user_id>", views.unfollow, name="unfollow_user"),
    path("follow/<int:profile_user_id>", views.follow, name="follow_user")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
