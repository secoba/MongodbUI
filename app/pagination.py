#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: pagination.py


from django.core.paginator import Paginator, EmptyPage

from logger import log_error


def paginator_tool(pages, queryset, display_amount=10, pernum=2):
    paginator = Paginator(queryset, display_amount)
    try:
        # 获取request中的page参数
        page = int(pages)
    except Exception as e:
        # 默认为1
        page = 1
        log_error("paginator get pages err %s" % e)

    try:
        # 尝试获得分页列表
        objects = paginator.page(page)
    except EmptyPage:
        # 如果页数不存在,获得最后一页
        objects = paginator.page(paginator.num_pages)
    except Exception as ex:
        # 如果不是一个整数，获得第一页
        objects = paginator.page(1)
        log_error("paginator get page err %s" % ex)

    # 根据参数配置导航显示范围
    page_range = None
    if page == 1:
        if page + pernum < paginator.num_pages:
            page_range = range(1, page + pernum + 1)
        else:
            page_range = range(1, paginator.num_pages + 1)
    elif 1 < page < paginator.num_pages:
        page_range = range(page - 1, page + pernum - 1 + 1)
    elif page == paginator.num_pages and paginator.num_pages == 2:
        page_range = range(page - 1, page + pernum - 2 + 1)
    elif page == paginator.num_pages and paginator.num_pages > 2:
        page_range = range(page - 2, page + pernum - 2 + 1)

    return objects, page_range
