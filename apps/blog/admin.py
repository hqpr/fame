from django.contrib import admin
from suit.admin import SortableTabularInline

from apps.blog.models import BlogItem,BlogAuthor,BlogCategory,BlogItemCategory,BlogTag,BlogItemTag,BlogItemComment,\
                    BlogCompetitionLinks


# Register your models here.
class BlogItemAuthorInline(SortableTabularInline):
    model = BlogAuthor
    suit_classes = 'suit-tab suit-tab-general'
    sortable = 'ordering'


class BlogItemCategoryInline(admin.TabularInline):
    model = BlogItemCategory
    suit_classes = 'suit-tab suit-tab-categories'

class BlogItemTagInline(admin.TabularInline):
    model = BlogItemTag
    suit_classes = 'suit-tab suit-tab-categories'

class BlogItemCommentInline(admin.TabularInline):
    model = BlogItemComment
    suit_classes = 'suit-tab suit-tab-comments'

class BlogCompetitionLinksInline(admin.TabularInline):
    model = BlogCompetitionLinks
    suit_classes = 'suit-tab suit-tab-categories'


class BlogItemAdmin(admin.ModelAdmin):
    model = BlogItem
    suit_form_tabs = (('general', 'General'), ('categories', 'Categories & Tags'), ('comments','Comments'))
    inlines = [BlogItemAuthorInline, BlogItemCategoryInline,BlogItemTagInline,BlogCompetitionLinksInline,BlogItemCommentInline]

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['title','slug','publish_date','published','content','snippet','thumbnail','cover_image','comments_open','featured',]
        }),
    ]

    list_display = ["title","slug","blog_categories","blog_tags","published","publish_date"]

    def blog_categories(self, obj):
        categories = BlogItemCategory.objects.filter(blog_item=obj)
        return ",".join([i.blog_category.title for i in categories])

    def blog_tags(self, obj):
        tags = BlogItemTag.objects.filter(blog_item=obj)
        return ",".join([i.blog_tag.title for i in tags])

class BlogCategoryAdmin(admin.ModelAdmin):
    model = BlogCategory

class BlogTagAdmin(admin.ModelAdmin):
    model = BlogTag

admin.site.register(BlogItem, BlogItemAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogTag, BlogTagAdmin)