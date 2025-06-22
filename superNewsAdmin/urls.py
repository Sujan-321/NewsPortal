from django.urls import path
from superNewsAdmin.views import *

app_name = "superNewsAdmin"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/edit/', RecipeUpdateView.as_view(), name='post-edit'),
    path('create-post/', PostCreateView.as_view(), name="createPost"),
    path('post-list/', PostListView.as_view(), name="postList"),
    path('category-list/', CategoryListView.as_view(), name="categoryList"),
]