from django.contrib import admin
from posts.models import Post, Author, PostAuthor, PostReview


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'created_at', 'is_approved' )
    list_filter = ('is_approved',)
    actions = ['approve_posts']
    search_fields = ('title',)

    def author(self, obj):
        post_author = PostAuthor.objects.filter(post=obj).first()
        return post_author.author.full_name() if post_author else "No Author"

    @admin.action(description="Select posts and approve them")
    def approve_posts(self, request, queryset):
        queryset.update(is_approved=True)




class AuthorAdmin(admin.ModelAdmin):
    pass

class PostAuthorAdmin(admin.ModelAdmin):
    pass

class PostReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PostAuthor, PostAuthorAdmin)
admin.site.register(PostReview, PostReviewAdmin)