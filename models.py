# -*- coding: utf-8 -*-
import time, random
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.pages.models import Page
from mezzanine.utils.models import base_concrete_model


class PagePost(Displayable, Ownable, RichText, AdminThumbMixin):
    """
    A category page post.
    """

    category = models.ForeignKey("Category",
                                    verbose_name=_("Categories"))
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    # rating = RatingField(verbose_name=_("Rating"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("PagePost.featured_image", "page"),
        format="Image", max_length=255, null=True, blank=True)
    # related_posts = models.ManyToManyField("self",
    #                              verbose_name=_("Related posts"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = _("Category page")
        verbose_name_plural = _("Category pages")
        ordering = ("category", "publish_date")

    @models.permalink
    def get_absolute_url(self):
        url_name = "page_post_detail"
        kwargs = {"slug": self.slug}

        return (url_name, (), kwargs)

    def category_list(self):
        return getattr(self, "_category", self.category_set.all())

    def keyword_list(self):
        try:
            return self._keywords
        except AttributeError:
            keywords = [k.keyword for k in self.keywords.all()]
            setattr(self, "_keywords", keywords)
            return self._keywords

    def _get_next_or_previous_by_category(self, is_next, **kwargs):
        """
        Retrieves next or previous object by publish date. We implement
        our own version instead of Django's so we can hook into the
        published manager and concrete subclasses.
        """
        arg = "publish_date__gt" if is_next else "publish_date__lt"
        order = "publish_date" if is_next else "-publish_date"
        lookup = {arg: self.publish_date, "category_id": self.category_id}
        concrete_model = base_concrete_model(Displayable, self)
        try:
            queryset = concrete_model.objects.published
        except AttributeError:
            queryset = concrete_model.objects.all
        try:
            return queryset(**kwargs).filter(**lookup).order_by(order)[0]
        except IndexError:
            pass

    def get_next_by_category(self, **kwargs):
        """
        Retrieves next object by publish date.
        """
        return self._get_next_or_previous_by_category(True, **kwargs)

    def get_previous_by_category(self, **kwargs):
        """
        Retrieves previous object by publish date.
        """
        return self._get_next_or_previous_by_category(False, **kwargs)

    def save(self, *args, **kwargs):
        if self.slug == "":
            now = time.localtime(time.time())
            self.slug = time.strftime('%y%m%d%H%M%S', now) + str(random.randint(0, 99))
        super(self.__class__, self).save(*args, ** kwargs)


class Category(Page, Slugged):
    """
    A category for grouping category page posts into a series.
    """
    # title = models.CharField(_("Title"), max_length=500, unique=True)
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("title",)

    # @models.permalink
    # def get_absolute_url(self):
    #     return ("list_category", ())
