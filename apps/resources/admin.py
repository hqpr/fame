from django.contrib import admin
from suit.admin import SortableTabularInline

from .models import ResourcesItem, ResourcesAuthor, ResourcesCategory, ResourcesItemCategory, ResourcesTag,\
    ResourcesItemTag, ResourcesItemComment, ResourcesCompetitionLinks


class ResourcesItemAuthorInline(SortableTabularInline):
    model = ResourcesAuthor
    suit_classes = 'suit-tab suit-tab-general'
    sortable = 'ordering'


class ResourcesItemCategoryInline(admin.TabularInline):
    model = ResourcesItemCategory
    suit_classes = 'suit-tab suit-tab-categories'

class ResourcesItemTagInline(admin.TabularInline):
    model = ResourcesItemTag
    suit_classes = 'suit-tab suit-tab-categories'

class ResourcesItemCommentInline(admin.TabularInline):
    model = ResourcesItemComment
    suit_classes = 'suit-tab suit-tab-comments'

class ResourcesCompetitionLinksInline(admin.TabularInline):
    model = ResourcesCompetitionLinks
    suit_classes = 'suit-tab suit-tab-categories'


class ResourcesItemAdmin(admin.ModelAdmin):
    model = ResourcesItem
    suit_form_tabs = (('general', 'General'), ('categories', 'Categories & Tags'), ('comments', 'Comments'))
    inlines = [ResourcesItemAuthorInline, ResourcesItemCategoryInline, ResourcesItemTagInline,
               ResourcesCompetitionLinksInline, ResourcesItemCommentInline]

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['title', 'slug', 'publish_date', 'published', 'content', 'snippet', 'thumbnail',
                       'cover_image', 'comments_open', 'featured', ]
        }),
    ]

    list_display = ["title", "slug", "resource_categories", "resource_tags", "published", "publish_date"]

    def resource_categories(self, obj):
        categories = ResourcesItemCategory.objects.filter(resource_item=obj)
        return ",".join([i.resource_category.title for i in categories])

    def resource_tags(self, obj):
        tags = ResourcesItemTag.objects.filter(resource_item=obj)
        return ",".join([i.resource_tag.title for i in tags])

class ResourcesCategoryAdmin(admin.ModelAdmin):
    model = ResourcesCategory

class ResourcesTagAdmin(admin.ModelAdmin):
    model = ResourcesTag

admin.site.register(ResourcesItem, ResourcesItemAdmin)
admin.site.register(ResourcesCategory, ResourcesCategoryAdmin)
admin.site.register(ResourcesTag, ResourcesTagAdmin)
