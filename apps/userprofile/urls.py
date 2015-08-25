from django.conf.urls import url

from apps.userprofile.views import login_view, logout_view, RegistrationView, check_username, RegistrationStepView, \
    upload_avatar, complete_registration, SocialView

urlpatterns = [
    url(r'^login/$', login_view, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$', RegistrationView.as_view(), name="register"),
    url(r'^register/(?P<object_id>\d+)/$', RegistrationStepView.as_view(), name="register_step_2"),
    url(r'^register/complete/$', complete_registration, name="complete_registration"),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/user/password/reset/done/'}, name="password_reset"),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/'}, name='password_reset_confirm'),
    url(r'^password/done/$', 'django.contrib.auth.views.password_reset_complete'),

    # services
    url(r'^check_username/$', check_username, name="check_username"),
    url(r'^avatar/(?P<object_id>\d+)/$', upload_avatar, name="upload_avatar"),

    # edit services
    url(r'^social/edit/$', SocialView.as_view(), name='edit_social'),
]

