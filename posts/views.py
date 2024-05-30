from .forms import PostCreation, CommentCreation
from .models import Posts, Comments
from allauth.account.decorators import verified_email_required, login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image


# tested
@verified_email_required
@login_required
def add_post(request):
    """creating a new post and adding it to
    db if request is post else show a post creating form"""

    if request.method == "POST":
        form = PostCreation(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            if form.cleaned_data.get("uploaded_image"):
                image = Image.open(instance.uploaded_image)
                image = image.resize((500, 500), Image.LANCZOS)
                image_io = BytesIO()
                image.save(image_io, format="PNG", quality=100)
                image_file = ContentFile(
                    image_io.getvalue(), name=instance.uploaded_image.name
                )
                instance.uploaded_image = image_file
                instance.save()
            form.save_m2m()
            messages.success(request, "Posted successfully")
            return redirect("home")
    else:
        form = PostCreation()

    return render(request, "posts/add_post.html", {"form": form})


# tested
@verified_email_required
@login_required
def post_detail(request, pk):
    """showing a post by its pk"""

    post = Posts.objects.get(pk=pk)
    tags = post.tags.all()
    comment_form = CommentCreation()
    comments = Comments.objects.filter(post=post)
    related_posts = Posts.objects.filter(tags__in=tags).exclude(id=pk).distinct()[:5]

    context = {
        "post": post,
        "tags": tags,
        "comment_form": comment_form,
        "comments": comments,
        "related_posts": related_posts,
    }
    return render(request, "posts/post_detail.html", context)


# tested
@verified_email_required
@login_required
def edit_post(request, pk):
    """get a post from db using it pk edit it then save back to db"""

    is_hx_request = request.headers.get("HX-Request") == "true"
    post = get_object_or_404(Posts, id=pk)
    post_id = post.id
    form = PostCreation(instance=post)
    if request.method == "POST":
        form = PostCreation(request.POST, request.FILES, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            if "uploaded_image" in request.FILES:
                instance.uploaded_image = request.FILES["uploaded_image"]
            instance.save()
            form.save_m2m()
            messages.success(request, "updated successfully")
            return redirect("post_detail", post_id)
    return render(
        request,
        "posts/edit_post.html",
        {"form": form, "post": post, "is_hx_request": is_hx_request},
    )


# tested
@verified_email_required
@login_required
def delete_post(request, pk):
    """delete a post using it pk"""

    post = get_object_or_404(Posts, id=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "deleted successfully")
        return redirect("home")
    else:
        return render(request, "snippets/delete_post.html", {"post": post})


# tested
@login_required
def tag_view(request, slug):
    """show all posts that have the tag passed in them"""

    is_hx_request = request.headers.get("HX-Request") == "true"
    posts = Posts.objects.filter(tags__slug=slug)
    if posts:
        return render(
            request,
            "core/home.html",
            {
                "all_posts": posts,
                "is_hx_request": is_hx_request,
            },
        )
    else:
        return HttpResponse("<h3 style='color: gray;' >Empty tag</h3>")


@login_required
@verified_email_required
def add_comment(request, pk):
    """add a comment to a post"""

    post = get_object_or_404(Posts, id=pk)
    if request.method == "POST":
        form = CommentCreation(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.author = request.user
            instance.save()
            return redirect("post_detail", pk)

    return render(request, "posts/add_comment.html", {"form": form})


def edit_comment(request, pk):
    """edit a comment using it pk"""

    comment = get_object_or_404(Comments, id=pk)
    post_id = comment.post.id

    if request.method == "POST":
        form = CommentCreation(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id)
    else:
        form = CommentCreation(instance=comment)
    return render(
        request, "posts/edit_comment.html", {"form": form, "comment": comment}
    )


def delete_comment(request, pk):
    """delete a comment using it pk"""

    comment = get_object_or_404(Comments, id=pk)
    post_id = comment.post.id

    if request.method == "POST":
        comment.delete()
        return redirect("post_detail", post_id)
    else:
        return render(request, "snippets/delete_comment.html", {"comment": comment})


def like_post(request, pk):
    """like a post"""

    post = get_object_or_404(Posts, id=pk)
    user = request.user
    if user != post.author:
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
    return redirect("post_detail", pk)


def like_comment(request, pk):
    """like a comment"""

    comment = get_object_or_404(Comments, id=pk)
    user = request.user
    if user != comment.author:
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
    return redirect("post_detail", comment.post.id)


def bookmark_post(request, pk):
    """bookmark a post"""

    post = get_object_or_404(Posts, id=pk)
    user = request.user
    if user != post.author:
        if user in post.bookmarks.all():
            post.bookmarks.remove(user)
        else:
            post.bookmarks.add(user)
    return redirect("post_detail", post.id)
