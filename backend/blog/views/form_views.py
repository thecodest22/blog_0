from django.views.generic import ListView

from blog.models import Post, Section


class PostListView(ListView):
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    queryset = (
        Post
        .objects
        .select_related('section')
        .only('title', 'annotation', 'picture', 'created_at', 'section__title')
    )
    extra_context = {'title': 'Главная страница'}
