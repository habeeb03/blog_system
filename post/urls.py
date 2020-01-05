from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostListView.as_view(), name="list"),
    path('blog-category/<category_slug>', views.PostByCategory.as_view(), name="category"),
    path('blog/<post_slug>', views.PostDetailView.as_view(), name="detail"),
    path('user/reaction', views.reaction, name='reaction'),
]
