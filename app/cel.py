#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020/5/15
# File: cel.py


import ast


class ValidErr(Exception):
    def __init__(self, *args):
        self.args = args


conn = {}
attr = []

OP_MAP = {
    ast.Gt: "$gt",
    ast.GtE: "$gte",
    ast.Lt: "$lt",
    ast.LtE: "$lte"
}

ALLOW_OP = [ast.Gt, ast.GtE, ast.Lt, ast.LtE, ast.Eq, ast.NotEq]


def get_attr(left_attr):
    global attr
    if isinstance(left_attr.__dict__.get("value"), ast.Attribute):
        attr.append(left_attr.__dict__.get("attr"))
        get_attr(left_attr.__dict__.get("value"))
    else:
        attr.append(left_attr.__dict__.get("attr"))
        attr.append(left_attr.__dict__.get("value").__dict__.get("id"))
    return ".".join(reversed(attr))


def get_val(node):
    if isinstance(node, ast.Compare):
        op = node.__dict__.get("ops")[0]
        left = node.__dict__.get("left")
        if isinstance(left, ast.Attribute):
            left_val = get_attr(left)
        else:
            if not isinstance(left, ast.Name):
                raise ValidErr("expr left type err, must be ast.Name")
            if type(op) not in ALLOW_OP:
                raise ValidErr("expr op not support")
            left_val = left.__dict__.get("id")
        right = node.__dict__.get("comparators")[0]
        right_val = right.__dict__.get("s") if isinstance(right, ast.Str) else right.__dict__.get("n")
        if isinstance(op, ast.Eq):
            return {left_val: right_val}
        elif isinstance(op, ast.NotEq):
            return {left_val: {"$ne": right_val}}
        else:
            # {"$gte": self.hourBegin, "$lte": self.now}
            return {left_val: {OP_MAP.get(type(op)): right_val}}
    raise ValidErr("expr must be ast.Compare")


def handle(node, ind=0, _list=[]):
    global conn
    if isinstance(node, ast.Compare):
        if ind == 0:
            conn = get_val(node)
        else:
            _list.append(get_val(node))
    elif isinstance(node, ast.BoolOp):
        node_list = []
        node_type = node.__dict__.get("op")
        if isinstance(node_type, ast.And) or isinstance(node_type, ast.Or):
            if isinstance(node_type, ast.And):
                _list.append({"$and": node_list})
            else:
                _list.append({"$or": node_list})
        else:
            raise ValidErr("expr type must be ast.And or ast.Or")
        if ind == 0:
            ind += 1
            conn = {"$and": node_list} if isinstance(
                node_type, ast.And) else {"$or": node_list}
            for i in node.__dict__.get("values"):
                handle(i, ind, node_list)
        else:
            ind += 1
            for i in node.__dict__.get("values"):
                handle(i, ind, node_list)
    else:
        raise ValidErr("expr type must be ast.Compare or ast.BoolOp")


def parser_expr(expr_string):
    global conn
    global attr
    conn.clear()
    attr.clear()
    conn = {}
    node = ast.parse(expr_string.strip()
                     .replace("&&", " and ")
                     .replace("||", " or ")).body[0].value
    handle(node=node, ind=0, _list=[])
    return conn


if __name__ == '__main__':
    print(parser_expr("test1.name1==123"))
    print(parser_expr("test2.name2.demo2=='aaa'"))
