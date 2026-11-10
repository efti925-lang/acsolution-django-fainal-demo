from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.template.response import TemplateResponse
from accounts.views import home_view
from .sitemaps import StaticSitemap, ProjectSitemap

sitemaps = {
    'static': StaticSitemap,
    'projects': ProjectSitemap,
}


def robots_txt(request):
    return TemplateResponse(request, 'robots.txt', {
        'scheme': request.scheme,
        'host': request.get_host(),
    }, content_type='text/plain')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('', include('showcase.urls')),
]

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='serve_media'),
]
