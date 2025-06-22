from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, View, UpdateView
from newspaper.models import Post, Category
from django.urls import reverse_lazy
from superNewsAdmin.forms import PostForm, CategoryForm
from django.urls import reverse
# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = "newsAdmin/home.html"
    context_object_name = "posts"
    paginate_by = 7

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")


class RecipeUpdateView(UpdateView):
    model = Post
    template_name = "newsAdmin/post_edit.html"
    form_class = PostForm

    def get_success_url(self):
        post = self.get_object()
        if post.created_at:
            return reverse("detailView", kwargs={"pk":post.pk})
        else:
            return reverse("home", kwargs={"pk": post.pk})

class PostDeleteView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect("superNewsAdmin:home")

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "newsAdmin/post_form.html"

    def form_valid(self, form):
        print("Form is valid! Saving instance...")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form invalid with errors:", form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("superNewsAdmin:home")


class PostListView(ListView):
    model=Post
    template_name="newsAdmin/post.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")

class CategoryListView(ListView):
    model=Category
    template_name="newsAdmin/category/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return super().get_queryset()