from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post, Status
from django.urls import reverse_lazy


# List of published posts view
class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = Status.objects.get(id=1)
        context["post_list"] = Post.objects.filter(
            status=status).order_by("created_on").reverse()
        return context

# List of draft posts view
class DraftPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = Status.objects.get(id=2)
        context["post_list"] = Post.objects.filter(
            status=status).filter(author=self.request.user).order_by("created_on").reverse()
        return context

# Posts detail view
class PostDetailView(DetailView):
    template_name = "posts/detail.html"
    model = Post

# New post view
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ['title', 'subtitle', 'body', 'status']

    # it is called whenever we submit the form
    def form_valid(self, form):
        # the author field is set to the usern's id
        form.instance.author = self.request.user
        # calls the original form to update it
        return super().form_valid(form)

# Update post view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ['title', 'subtitle', 'author', 'body', 'status']

    def test_func(self):
        post_obj = self.get_object()
        return self.request.user == post_obj.author

# Delete post view
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy('list')

    def test_func(self):
        post_obj = self.get_object()
        return self.request.user == post_obj.author