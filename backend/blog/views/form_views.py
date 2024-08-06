from django.views.generic import DetailView, ListView

from blog.models import Post


class PostListView(ListView):
    """
    Список постов.
    """
    queryset = (
        Post
        .objects
        .select_related('section')
        .only('title', 'annotation', 'picture', 'created_at', 'section__title')
    )
    extra_context = {'title': 'Список постов'}


class PostDetailView(DetailView):
    """
    Детали поста.
    """

    queryset = Post.objects.select_related('section')
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title

        return context
