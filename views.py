# -*- coding: utf-8 -*-
from calendar import month_name
from collections import defaultdict

from django.http import Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, get_list_or_404
from django import VERSION

from .models import PagePost, Category
from mezzanine.pages.models import RichTextPage
# from mezzanine.blog.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import AssignedKeyword, Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model

User = get_user_model()


def page_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="page_post_list.html"):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    page_posts = PagePost.objects.published(for_user=request.user)

    page_posts = paginate(page_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    author = None
    context = {"page_posts": page_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return render(request, templates, context)


def page_post_detail(request, slug, year=None, month=None, day=None,
                     template="category_page_post_detail.html"):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    page_posts = PagePost.objects.published(
                                     for_user=request.user)#.select_related()
    page_post = get_object_or_404(page_posts, slug=slug)
    context = {"page_post": page_post}
    templates = [u"category_page_post_detail", template]
    return render(request, templates, context)


def category_page_post_list(request, slug, tag=None, year=None, month=None, username=None,
                   category=None, template="category_page_post_list.html"):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """

    settings.use_editable()
    templates = []

    category = Category.objects.get(slug=slug)
    try:
        summary = RichTextPage.objects.get(parent=category)
    except:
        summary = None

    page_posts = PagePost.objects.published(for_user=request.user)

    try:
        page_posts = get_list_or_404(page_posts, category=category)
    except:
        # return HttpResponse(u"没有找到记录")
        page_posts = []

    # item_per_page = {'tour': 6, 'estate': 6, 'project': 2, 'listing': 6}

    page_posts = paginate(page_posts, request.GET.get("page", 1),
                          16,# settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    author = None
    context = {"page_posts": page_posts, "year": year, "month": month,
                "tag": tag, "category": category, "author": author,
                "slug": slug, "summary": summary }
    templates = [u"category_page_post_list.html", template]
    return render(request, templates, context)