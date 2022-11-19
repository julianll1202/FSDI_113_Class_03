from django.views.generic import CreateView

class PostListView(CreateView):
    template_name = "posts/list.html"