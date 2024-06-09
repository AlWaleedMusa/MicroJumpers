from .models import Profile
from .forms import EditProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Posts, Comments


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()


def show_user(request, username):
    """Show user profile"""

    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    confirmed_solutions = Comments.objects.filter(
        author=request.user, mark_solution=True
    ).count()
    is_hx_request = request.headers.get("HX-Request") == "true"

    if request.user.username == username:

        context = {
            "profile": profile,
            "confirmed_solutions": confirmed_solutions,
            "is_hx_request": is_hx_request,
        }
        return render(request, "profiles/show_user.html", context)
    else:
        context = {
            "profile": profile,
        }
        return render(request, "profiles/show_profile.html", context)


def bookmarks(request, username):
    """Show user bookmarks"""

    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmarked_posts.all()

    context = {
        "bookmarks": bookmarks,
    }

    return render(request, "snippets/bookmarks.html", context)


def user_posts(request, username):
    """Show user posts"""

    user = get_object_or_404(User, username=username)
    posts = Posts.objects.filter(author=user)

    context = {
        "posts": posts,
    }

    return render(request, "snippets/user_posts.html", context)


@login_required
def search_profile(request, username):
    """Search page"""

    q = request.GET.get("search", None)
    posts = Posts.objects.filter(author__username=username)

    if q:
        posts = posts.filter(
            Q(title__icontains=q) | Q(body__icontains=q) | Q(tags__name__icontains=q)
        ).distinct()

    return render(
        request, "snippets/profile_search.html", {"post_search_result": posts}
    )


def profile_settings(request, username):
    """Profile settings"""

    context = {
        "profile": Profile.objects.get(user=request.user),
    }

    return render(request, "snippets/profile_settings.html", context)


def edit_profile(request, username):
    """Edit profile settings"""

    profile = get_object_or_404(User, username=username)
    user = request.user
    if request.method == "POST":
        form = EditProfile(
            request.POST, request.FILES, instance=profile.user_profile, user=user
        )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            # updating userModel data
            user_instance = user
            user_instance.username = form.cleaned_data["username"]
            user_instance.first_name = form.cleaned_data["first_name"]
            user_instance.last_name = form.cleaned_data["last_name"]
            user_instance.save()
            return redirect("show_user", username=user.username)

    form = EditProfile(instance=profile.user_profile, user=user)
    return render(request, "profiles/edit_profile_settings.html", {"form": form})
