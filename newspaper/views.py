from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import *
from newspaper.models import Post, Advertisement, Tag, Category, OurTeam
from django.utils import timezone
from datetime import timedelta
from newspaper.forms import ContactForm, CommentForm, NewsletterForm
from newspaper.models import Contact
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.


class SideBarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # it returns the dictionary data

        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]

        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )

        print(f"\n\n\n\nthe context contain: \n\n\n{context}\n\n\n\n")

        return context


class HomeView(SideBarMixin, ListView):
    model = Post
    template_name = "newsportal/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")[:4]

    # for providing extra data to template we need to use 'get_context_data()'
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)  # it returns the dictionary data
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )

        # context["popular_posts"] = Post.objects.filter(
        #     published_at__isnull=False, status="active"
        # ).order_by("-published_at")[:5]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at", "-views_count")[:5]

        # context["advertisement"] = (
        #     Advertisement.objects.all().order_by("-created_at").first()
        # )

        context["breaking_news"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:3]

        print(f"\n\n\n\nthe context contain: \n\n\n{context}\n\n\n\n")

        return context


class PostListView(SideBarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")


class PostDetailView(DetailView):
    model = Post
    template_name = "newsportal/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = self.object
        current_post.views_count += 1
        current_post.save()

        post = self.get_object()
        context["related_posts"] = (
            Post.objects.filter(
                published_at__isnull=False, status="active", category=post.category
            )
            .exclude(pk=post.pk)
            .order_by("-published_at", "-views_count")[:2]
        )
        return context



class PostByCategory(SideBarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginated_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            category__id=self.kwargs["category_id"],
        ).order_by("-published_at")
        return query
    


class TagListView(ListView):
    model = Tag
    template_name = "newsportal/tags.html"
    context_object_name = "tags"


class CategoryListView(ListView):
    model = Category
    template_name = "newsportal/categories.html"
    context_object_name = "categories"



# class OurTeamListView(ListView):
#     model = OurTeam
#     template_name = "newsportal/about.html"
#     context_object_name = "teams"


class AboutView(TemplateView):
    template_name = "newsportal/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["our_teams"] = OurTeam.objects.all()
        return context





from django.urls import reverse_lazy  # module level import not at top of file
from django.contrib.messages.views import SuccessMessageMixin

class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = "newsportal/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully!"



class CommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST["post"]

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("postDetail", post_id)
        else:
            post = Post.objects.get(pk=post_id)

            popular_posts = Post.objects.filter(
                published_at__isnull=False, status="active"
            ).order_by("-published_at")[:5]
            advertisement = Advertisement.objects.all().order_by("-created_at").first()
            return render(
                request,
                "newsportal/detail/detail.html",
                {
                    "post":post,
                    "form":form,
                    "popular_posts": popular_posts,
                    "advertisement": advertisement,
                },

            )




class NewsletterView(View):
    def post(self, request):
        is_ajax = request.headers.get("x-requested-with")

        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Successfully subscribed to the newsletter.",
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {
                        "success":False,
                        "message": "Cannot subscribe to the newsletter.",
                    },
                    status=400
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX XMLHttpRequest",
                },
                status=400
            )






class PostSearchView(View):
    template_name = "newsportal/list/list.html"

    def get(self, request, *args, **kwargs):
        print(request.GET)
        query = request.GET["query"]    # nepal=> NePal
        post_list = Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query))
            & Q(status="active")
            & Q(published_at__isnull=False)
        ).order_by(
            "-published_at"
        ) # queryset => ORM

        # pagination start
        page = request.GET.get("page", 1)   # it avoid error genera
        paginate_by = 1
        paginator = paginator(post_list, paginate_by)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
            # pagination end
    
    popular_posts = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")[:5]
    advertisement = Advertisement.objects.all().order_by("-created_at").first()


    # return render(
    #     request,
    #     self.template_name,
    #     {
    #         "page_obj": posts,
    #         "query":query,
    #         "popular_posts": popular_posts,
    #         "advertisement": advertisement,
    #     },
    # )

