from django.shortcuts import render, get_object_or_404

from .models import ResourcesItem, ResourcesAuthor, ResourcesItemCategory, ResourcesItemTag, ResourcesItemComment


def resources(request):
    filter_dictionary = {}
    if request.GET.get("category"):
        filter_dictionary["resourcesitemcategory__resource_category__slug"] = request.GET["category"]
    if request.GET.get("tag"):
        filter_dictionary["resourcesitemtag__resource_tag__slug"] = request.GET["tag"]

    featured_resources = ResourcesItem.published_objects.filter(**filter_dictionary). \
                             filter(featured=True).order_by("-publish_date")[:3]
    resources = ResourcesItem.published_objects.filter(**filter_dictionary).exclude(pk__in=[i.id for i in featured_resources]).order_by("-publish_date")
    
    template_data = {
        "featured_resources": featured_resources,
        "resources": resources
    }

    return render(request, 'resources.html', template_data)

def single_resource(request, *args, **kwargs):
    resource_item = get_object_or_404(ResourcesItem, slug=kwargs["slug"])
    resource_authors = ResourcesAuthor.objects.filter(resource_item=resource_item).order_by('ordering')
    resource_categories = ResourcesItemCategory.objects.filter(resource_item=resource_item)
    resource_tags = ResourcesItemTag.objects.filter(resource_item=resource_item)
    parent_comments = ResourcesItemComment.published_objects.filter(resource_item=resource_item, reply_to=None).\
        order_by('-created')
    
    resource_comments = []
    if parent_comments:
        for comment in parent_comments:
            sub_comments = ResourcesItemComment.published_objects.filter(resource_item=resource_item, reply_to=comment)
            resource_comments.append((comment, sub_comments))

    template_data = {
        "resource": resource_item,
        "resource_authors": resource_authors,
        "resource_categories": resource_categories,
        "resource_tags": resource_tags,
        "resource_comments": resource_comments,
    }
    return render(request, 'single-resource.html', template_data)
