import pytz
from datetime import datetime
from django import template
from django.conf import settings
register = template.Library()

from ..models import CompetitionStage

@register.inclusion_tag('partials/competition-status.html', takes_context=True)
def status(context, competition):
    competition_stages = CompetitionStage.objects.filter(competition=competition).order_by('ordering')
    total_competition_stages = len(competition_stages)
    current_date = datetime.now(tz=pytz.UTC)

    current_stage_texts = return_current_stage("pending")
    current_index = 0

    if current_date > competition.date_end:
        current_stage_texts = return_current_stage("ended")
        current_index = total_competition_stages + 1
    else:
        current_stage = ""
        for idx, competition_stage in enumerate(competition_stages):
            if competition_stage.date_start < current_date:
                current_stage = competition_stage
                current_index = idx + 1

        if current_stage:
            current_stage_texts = return_current_stage("process",current_stage,(float(current_index)/float(total_competition_stages)*100 - 1/(2*float(total_competition_stages))*100))

    # poll = Choice.objects.all()
    return {
        'competition_stages': competition_stages,
        'current_stage_texts': current_stage_texts,
        'current_stage_index': current_index,
        'stage_width': "%s%%" % ((1.0/len(competition_stages))*100),
        'MEDIA_URL': context['MEDIA_URL']
    }

def return_current_stage(value, dict={}, percentage_width=0):
    if value == "ended":
        return {"title": "Ended", "text": "This has ended", "percentage_width" : 100}
    elif value == "pending":
        return {"title": "Pending", "text": "This competition hasn't started yet", "percentage_width" : 0}
    return {"title": dict.name, "text": dict.description, "percentage_width" : percentage_width}
