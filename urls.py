
from django.conf.urls.defaults import patterns, url

from mezzanine.conf import settings

# Wiki patterns.
urlpatterns = patterns("mezzanine_category_page.views",
    url("^(?P<slug>.*)/pages/$", "category_page_post_list", name="category_page_post_list"),
    url("^(?P<slug>.*)/$", "page_post_detail", name="page_post_detail"),
    # url("^$", "page_post_list", name="page_post_list"),
)