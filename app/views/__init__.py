#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: __init__.py

from django.http import JsonResponse


def json_response(status, msg, data):
    return JsonResponse({"msg": msg, "data": data, "status": status})


def data_filter_list(query_list, includes=[]):
    result = []
    for item in query_list:
        item_dict = {}
        for k, v in item.__dict__.items():
            if k == "_state":
                continue
            if len(includes) == 0:
                result.append({k: v})
            else:
                if k in includes:
                    item_dict[k] = v
        result.append(item_dict)
    return result


def json_data_filter_list(json_data, fields=None, exclude=None):
    """
    获取json键值
    :param json_data:
    :param fields:
    :param exclude:
    :return: 返回list
    """
    data = list()
    if isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, dict):
                data_map = dict()
                for k, v in item.items():
                    if isinstance(exclude, list):
                        if k in exclude:
                            continue
                    if isinstance(fields, list):
                        if k in fields:
                            data_map[k] = v
                    else:
                        if k == "_id":
                            data_map[k] = str(v)
                        else:
                            data_map[k] = v
                data.append(data_map)
    return data


class STATUS:
    Ok = 0
    Err = 1
