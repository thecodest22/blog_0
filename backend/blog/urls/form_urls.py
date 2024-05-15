from django.urls import path

from blog.views.form_views import PostDetailView, PostListView

app_name = 'blog'

urlpatterns = [
    path(
        'posts/',
        PostListView.as_view(),
        name='post_list'
    ),
    path(
        'posts/<slug:post_slug>/',
        PostDetailView.as_view(),
        name='post_detail'
    ),
]
