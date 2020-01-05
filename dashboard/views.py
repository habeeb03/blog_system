from django.shortcuts import render, reverse
from django.views.generic import View, ListView
from post.models import Post

from django.http import HttpResponse, HttpResponseRedirect


class DasboardView(ListView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            post_count = Post.objects.filter(author=request.user).count
            likes_count = 10
            comment_count = 10
            context = {
                'post_count': post_count,
                'likes_count': likes_count,
                'comments_count': comment_count,
            }
            return render(request, 'dashboard/dashboard.html', context)

        return HttpResponseRedirect(reverse('post:list'))
