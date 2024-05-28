from allauth.account.decorators import verified_email_required, login_required
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from posts.models import Posts


# tested
def landing_page(request):
    """Render the landing page."""
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "core/landing_page.html")


# tested
@login_required
def home(request):
    """Render the home page."""

    is_hx_request = request.headers.get("HX-Request") == "true"
    all_posts = Posts.objects.all()[:10]
    return render(
        request,
        "core/home.html",
        {"all_posts": all_posts, "is_hx_request": is_hx_request},
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
