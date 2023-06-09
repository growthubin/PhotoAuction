"""
URL configuration for PhotoAuction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from content.views import Main, SearchResult, PostForm
from .views import Chapter1, Chapter2, Chapter3

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Main.as_view(), name='main'),
    path("search/", SearchResult.as_view(), name='search_result'),
    path("submit/", PostForm.as_view(), name='submit'),
    path("chapter1", Chapter1.as_view(), name='chapter1'),
    path("chapter2", Chapter2.as_view(), name='chapter2'),
    path("chapter3", Chapter3.as_view(), name='chapter3')
]
