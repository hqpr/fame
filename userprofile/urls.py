from django.conf.urls import url
from .views import login_view, logout_view, RegistrationView, check_username

urlpatterns = [
    url(r'^login/$', login_view, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^check_username/$', check_username, name="check_username"),
    url(r'^register/$', RegistrationView.as_view(), name="register"),
    # url(r'^register/(?P<object_id>\d+)/$', RegistrationStepView.as_view(), name="register_step_2"),
]

