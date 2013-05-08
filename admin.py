
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine_category_page.models import PagePost, Category
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from django.conf.urls.defaults import patterns, url


pagepost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
pagepost_fieldsets[0][1]["fields"].insert(1, "category")
pagepost_fieldsets[0][1]["fields"].extend(["content", "allow_comments"])
pagepost_list_display = ["title", "category", "user", "status", "admin_link"]
if settings.BLOG_USE_FEATURED_IMAGE:
    pagepost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    pagepost_list_display.insert(0, "admin_thumb")
pagepost_fieldsets = list(pagepost_fieldsets)
# pagepost_fieldsets.insert(1, (_("Other posts"), {
#     "classes": ("collapse-closed",),
#     "fields": ("related_posts",)}))


class PagePostAdmin(DisplayableAdmin, OwnableAdmin):
    """
    Admin class for blog posts.
    """

    fieldsets = pagepost_fieldsets
    list_display = pagepost_list_display
    # filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


category_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin class for blog categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    # fieldsets = ((None, {"fields": ("title",)}),)
    fieldsets = category_fieldsets
    list_display = ["title"]

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        # for (name, items) in settings.ADMIN_MENU_ORDER:
        #     if "blog.BlogCategory" in items:
        #         return True
        return False


admin.site.register(PagePost, PagePostAdmin)
admin.site.register(Category, CategoryAdmin)
