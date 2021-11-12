from django.urls import path
from .views import (
    PodcastsView, PodcastAllView, PodcastUserSpecific, SearchPodcast, PodcastSpecific)

urlpatterns = [
    path('',
         PodcastsView.as_view(),
         name="podcasts"
         ),

    path('<user_id>',
         PodcastUserSpecific.as_view(),
         name="Podcast User Specific"
         ),

    path('pod/<pod_id>',
         PodcastSpecific.as_view(),
         name="Podcast Specific"
         ),

    path('all/',
         PodcastAllView.as_view(),
         name="all Podcasts"
         ),

    path('search/',
         SearchPodcast.as_view(),
         name="Search Podcast"
         ),
]
