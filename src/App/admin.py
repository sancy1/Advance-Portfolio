from django.contrib import admin
from .models import Profile, About, Services, Experience, Blog, Category, Tag, Author, MyCv, Subscribe



class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'slug')
    prepopulated_fields = {'slug': ('title',), }

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug')
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Profile)
admin.site.register(About)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Experience)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(MyCv)
admin.site.register(Subscribe)