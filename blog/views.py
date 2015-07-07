from django.shortcuts import render, get_object_or_404
from .models import BlogItem,BlogAuthor,BlogCategory,BlogItemCategory,BlogTag,BlogItemTag,BlogItemComment

# Create your views here.
def blogs(request):
    filter_dictionary = {}
    if request.GET.get("category"):
        filter_dictionary["blogitemcategory__blog_category__slug"] = request.GET["category"]
    if request.GET.get("tag"):
        filter_dictionary["blogitemtag__blog_tag__slug"] = request.GET["tag"]

    featured_blogs = BlogItem.published_objects.filter(**filter_dictionary).filter(featured=True).order_by("-publish_date")[:3]
    blogs = BlogItem.published_objects.filter(**filter_dictionary).exclude(pk__in=[i.id for i in featured_blogs]).order_by("-publish_date")
    
    template_data = {
        "featured_blogs": featured_blogs,
        "blogs": blogs
    }

    return render(request, 'blogs.html', template_data)

def single_blog(request, *args, **kwargs):
    blog_item = get_object_or_404(BlogItem, slug=kwargs["slug"])
    blog_authors = BlogAuthor.objects.filter(blog_item=blog_item).order_by('ordering')
    blog_categories = BlogItemCategory.objects.filter(blog_item=blog_item)
    blog_tags = BlogItemTag.objects.filter(blog_item=blog_item)
    parent_comments = BlogItemComment.published_objects.filter(blog_item=blog_item,reply_to=None).order_by('-created')
    
    blog_comments = []
    if parent_comments:
        for comment in parent_comments:
            sub_comments = BlogItemComment.published_objects.filter(blog_item=blog_item,reply_to=comment)
            blog_comments.append((comment, sub_comments))

    template_data = {
        "blog": blog_item,
        "blog_authors": blog_authors,
        "blog_categories": blog_categories,
        "blog_tags": blog_tags,
        "blog_comments": blog_comments,
    }
    return render(request, 'single-blog.html', template_data)