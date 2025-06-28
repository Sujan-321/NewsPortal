from django.contrib import admin
from newspaper.models import Tag, Category, Post, Advertisement, UserProfile, Contact, Comment, OurTeam, Newsletter
from django_summernote.admin import SummernoteModelAdmin  # if using Summernote

# Register your models here.
admin.site.register(Tag)
admin.site.register(Category)
# admin.site.register(Post)
admin.site.register(Advertisement)
admin.site.register(UserProfile)
admin.site.register(OurTeam)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Newsletter)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)

admin.site.register(Post,PostAdmin)  # note that if 'Post' has registered already then remove that