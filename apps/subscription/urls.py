from django.conf.urls import url

from .views import subscripe_to_pro

urlpatterns = [
    url(r'^$', subscripe_to_pro, name='subscripe_to_pro'),
]

