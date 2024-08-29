from django.shortcuts import render

# Create your views here.

from Bot.slackapp  import slack_handler
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def slack_events(request):
    # if request.method == "POST":
    print("Incoming post request")
    return slack_handler.handle(request)
    
