from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View, DetailView
from .models import Post, Category, Comment, VistedIPs, ViewCount, Reaction
from django.core.paginator import Paginator
from blog.utils import get_client_ip
from django.http import HttpResponse, JsonResponse


class PostListView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.all()[:5],
            'featured_post': Post.objects.filter(featured=True)[:6],
            'posts': Post.objects.filter(featured=False),
            'title': 'Home',
        }
        return render(request, 'post/post_list.html', context)


class PostByCategory(View):
    def get(self, request, category_slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=category_slug)
        context = {
            'post': Post.objects.filter(category=category),
            'categories': Category.objects.all()[:5],
            'title': category
        }
        return render(request, 'post/post_by_category.html', context)


class PostDetailView(View):
    def get(self, request, post_slug, *args, **kwargs):
        post = get_object_or_404(Post, url=post_slug)
        comments = Comment.objects.filter(post=post)

        likes = Reaction.objects.filter(post=post, reaction=True).count

        
        ip = get_client_ip(request)
        total_views = 0

        try:
            current_views = ViewCount.objects.get(post=post)
            total_views = current_views.views
        except:
            current_views = ViewCount(post=post)

        try:
            is_visited = VistedIPs.objects.get(ip=ip)
        except:
            current_views.views += 1
            current_views.save()
            VistedIPs(ip=ip, post=post).save()

        context = {
            'post_details': post,
            'categories': Category.objects.all()[:5],
            'comments': comments,
            'title': post.title,
            'total_views': total_views,
            'total_likes': likes
        }

        return render(request, 'post/post_details.html', context)

    def post(self, request, post_slug, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, url=post_slug)
        comment_instanse = Comment(
            post=post, comment=request.POST['comment'], user=user)
        comment_instanse.save()

        comments = Comment.objects.filter(post=post)

        context = {
            'post_details': post,
            'categories': Category.objects.all()[:5],
            'comments': comments,
        }
        return render(request, 'post/post_details.html', context)


def reaction(request):
    user_reaction = request.POST['action']
    post = request.POST['post']
    post = Post.objects.get(pk=post)
    user = request.user

    is_liked = Reaction.objects.filter(post=post, user=user, reaction=1)

    is_disliked = Reaction.objects.filter(post=post, user=user, reaction=0)

    if(len(is_liked) == 0 and int(user_reaction) == 1):
        user_reaction = True
    elif(len(is_disliked) == 0 and int(user_reaction) == 0):
        user_reaction = False
    else:
        return JsonResponse({'status': False})

    Reaction(post=post, user=user, reaction=user_reaction).save()
    total_likes = Reaction.objects.filter(post=post)

    res = {
        'total_likes': len(total_likes),
        'status': True
    }

    return JsonResponse(res)
