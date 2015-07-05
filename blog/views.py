from django.shortcuts import render

# Create your views here.
def blogs(request):
    return render(request, 'blogs.html', {})

def single_blog(request, *args, **kwargs):
    return render(request, 'single-blog.html', {})