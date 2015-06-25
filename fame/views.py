from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate

# Create your views here.
def login(request):
    """View all login"""

    template_name = 'accounts/login.html'
    template_data = {
        "string": "Login Page",
    }

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                print("User is valid, active and authenticated")
                return redirect('profile')
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            print("The username and password were incorrect.")

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )

# Create your views here.
def register(request):
    """View register"""

    template_name = 'accounts/register.html'
    template_data = {
        "string": "Register Page",
    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )