from django.shortcuts import render
import simplejson
import stripe
from django.conf import settings
from django.http import HttpResponse
from .models import Subscription
from apps.userprofile.models import UserProfile
from datetime import timedelta
import datetime


def subscripe_to_pro(request):
    """ public key is in template """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        token = request.POST['stripeToken']
        stripe_amount = request.POST.get('stripe_amount', None)
        if not stripe_amount:
            stripe_amount = 20000
        try:
            stripe.Charge.create(
                amount=stripe_amount,  # amount in cents
                currency="usd",
                source=token,
                description='Payment from a website'
            )
            end_date = datetime.datetime.now() + timedelta(days=30)
            Subscription.objects.create(user=request.user, amount=stripe_amount, success=True,
                                        email=request.user.email, end_date=end_date)
            u = UserProfile.objects.get(user=request.user)
            u.is_pro = True
            u.save()
            data = {'success': True}
            return HttpResponse(simplejson.dumps(data), content_type='application/json')
        except Exception as e:
            Subscription.objects.create(user=request.user, amount=stripe_amount, success=False,
                                        email=request.user.email)
            data = {'success': False}
            print 'The card has been declined'
            print e
            return HttpResponse(simplejson.dumps(data), content_type='application/json')
    return render(request, 'settings.html', {})
