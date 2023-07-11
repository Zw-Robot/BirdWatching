#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-11:21:20
--------------------------------------------
"""
from flask import Blueprint
aviary = Blueprint('aviary', __name__)
from ..aviary import views