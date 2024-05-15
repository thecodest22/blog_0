from django.urls import path

from blog.views.form_views import PostListView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list')
]
