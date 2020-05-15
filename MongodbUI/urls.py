"""MongodbUI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views import static as st

from app import view

urlpatterns = [
    url(r"^$", view.index, name="index"),
    url(r"^data/", include("app.urls.data", namespace="data")),
    url(r"^config/", include("app.urls.config", namespace="config")),
    url(r'^static/(?P<path>.*)$', st.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
