from allauth.account.decorators import verified_email_required, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count, Sum
from posts.models import Posts, Comments
from taggit.models import Tag
from profiles.models import Profile


# tested
def landing_page(request):
    """Render the landing page with dynamic data for impact section"""
    users_count = User.objects.all().count
    solutions_count = Comments.objects.all().filter(mark_solution=True).count()

    tags_with_review = Tag.objects.filter(name__icontains="review")
    tags_with_review_count = tags_with_review.annotate(posts_count=Count('posts'))
    reviews_count = tags_with_review_count.aggregate(total_mentions=Sum('posts_count'))['total_mentions']
    
    all_countries = Profile.objects.exclude(location__isnull=True).values_list('location', flat=True)
    country_count = len(set(all_countries))
    
    context = {
        "user_count": users_count,
        "solutions_count": solutions_count,
        "reviews_count": reviews_count,
        "country_count": country_count
    }
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "core/landing_page.html", context)


# tested
@login_required
def home(request):
    """Render the home page."""

    is_hx_request = request.headers.get("HX-Request") == "true"
    all_posts = Posts.objects.all()[:10]
    user = get_object_or_404(User, username=request.user.username)
    profile = Profile.objects.get(user=user)
    return render(
        request,
        "core/home.html",
        {"all_posts": all_posts, "is_hx_request": is_hx_request, "profile": profile},
    )


@login_required
def search(request):
    """Search page"""

    is_hx_request = request.headers.get("HX-Request") == "true"
    q = request.GET.get("search", None)
    if q:
        posts = Posts.objects.filter(
            Q(title__icontains=q) | Q(body__icontains=q) | Q(tags__name__icontains=q)
        ).distinct()
    else:
        posts = Posts.objects.all()[:10]
        return render(
            request,
            "core/home.html",
            {"all_posts": posts, "is_hx_request": is_hx_request},
        )

    return render(
        request, "core/home.html", {"all_posts": posts, "is_hx_request": is_hx_request}
    )
