from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from showcase.models import ShowcaseProject


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['home', 'showcase_public_list']

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ShowcaseProject.objects.all()

    def location(self, obj):
        return reverse('showcase_public_detail', args=[obj.pk])

    def lastmod(self, obj):
        return obj.created_at
