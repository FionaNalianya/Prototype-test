from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('slack/events/',views.slack_events,name='slack-ents'),
    path('home/',TemplateView.as_view(template_name="index.html")),
    path('home/edit/',TemplateView.as_view(template_name="index.html")),
    # path('bot/',views.slack_events,name='slack-ents'),
]