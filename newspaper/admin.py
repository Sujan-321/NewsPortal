from django.contrib import admin
from newspaper.models import Tag, Category, Post, Advertisement, UserProfile, Contact, Comment, OurTeam, Newsletter

# Register your models here.
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Advertisement)
admin.site.register(UserProfile)
admin.site.register(OurTeam)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Newsletter)