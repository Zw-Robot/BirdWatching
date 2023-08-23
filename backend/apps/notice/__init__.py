#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-15:10:58
--------------------------------------------
"""
from flask import Blueprint

notice = Blueprint('notice', __name__)
from ..notice import views
