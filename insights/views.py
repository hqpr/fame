from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from social.apps.django_app.default.models import UserSocialAuth
import soundcloud
import tweepy
from django.conf import settings


@login_required
def artist_insights(request, *args, **kwargs):
    """View insights page"""
    try:
        token = UserSocialAuth.objects.get(user_id=request.user.id, provider='soundcloud')
        client = soundcloud.Client(use_ssl=False, access_token=token.access_token)
        tracks = client.get('/me/tracks')
    except UserSocialAuth.DoesNotExist:
        token = None
        tracks = None
    except:
        token = None
        tracks = None

    try:
        twitter_token = UserSocialAuth.objects.get(user_id=request.user.id, provider='twitter')
        auth = tweepy.OAuthHandler(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET)
        auth.set_access_token(twitter_token.access_token['oauth_token'], twitter_token.access_token['oauth_token_secret'])

        api = tweepy.API(auth)
        me = api.me()
        friends = me.friends_count
        followers = me.followers_count
        tweets = me.statuses_count
    except:
        friends = None
        followers = None
        tweets = None
        twitter_token = None

    template_name = 'insights.html'
    template_data = {
        "string": "Insights Page",
        'token': token,
        'tracks': tracks,
        'followers': followers,
        'friends': friends,
        'tweets': tweets,
        'twitter_token': twitter_token

    }

    return render_to_response(template_name,
                              template_data,
                              context_instance=RequestContext(request)
    )


