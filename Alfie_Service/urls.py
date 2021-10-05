"""Alfie_Service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from .apps.authentication import urls as authUrls
from .apps.podcasts import urls as podcastsUrls
from .apps.profiles import urls as profilesUrls
from .apps.blogs import urls as blogsUrls
from .apps.call_module import urls as callUrls
from .apps.subscriptions import urls as subscribeUrls
from .apps.payments.mpesa import urls as mpesaUrls

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'auth/',
        include(authUrls),
        name="authentication"),

    path(
        'podcasts/',
        include(podcastsUrls),
        name="podcasts"),

    path(
        'profiles/',
        include(profilesUrls),
        name="profiles"),

    path(
        'blog/',
        include(blogsUrls),
        name="blog"),

    path(
        'connect/',
        include(callUrls),
        name="DoctorRequest"),

    path(
        'subscribe/',
        include(subscribeUrls),
        name="=Subscribe"),

    path(
        'mpesa/',
        include(mpesaUrls),
        name="Mpesa Service"),
]