#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-09:11:57
--------------------------------------------
"""
def test(request):
    code = request.json.get('code')
    msg = ''
    json = {}
    return code,msg,json