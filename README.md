插件介绍
===================

用于mezzanine后台的文章分类

##配置
1、修改项目的urls.py，添加插件mezzanine_category_page的url映射：
###
    # MEZZANINE'S URLS
    # ----------------
    ("^category/", include("mezzanine_category_page.urls")),

2、修改项目的settings.py，将插件添加到面板中：
###
    ADMIN_MENU_ORDER = (
        ("Content", ("pages.Page", "blog.BlogPost",
            "mezzanine_category_page.PagePost", "mezzanine_category_page.Category",
            "generic.ThreadedComment", ("Media Library", "fb_browse"),)),
        ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
        ("Users", ("auth.User", "auth.Group",)),
    )

##扩展
