from django.urls import path
from newspaper.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post-list/", PostListView.as_view(), name="postList"),
    path("post-detail/<int:pk>/", PostDetailView.as_view(), name="postDetail"),
    path("category/<int:category_id>/", PostByCategory.as_view(), name="categoryDetail"),
    path("tag-list/", TagListView.as_view(), name="tagList"),
    path("category-list/", CategoryListView.as_view(), name="categoryList"),
    path("our-teams/", AboutView.as_view(), name="ourTeam"),
    path("contact/", ContactCreateView.as_view(), name="contact"),
    path("comment/", CommentView.as_view(), name="comment"),
    path("newsletter/", NewsletterView.as_view(), name="newsletter"),
    path("search/", PostSearchView.as_view(), name="search"),
]