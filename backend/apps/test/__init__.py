#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-09:11:56
--------------------------------------------
"""
from flask import Blueprint
test = Blueprint('test', __name__)
from ..test import urls