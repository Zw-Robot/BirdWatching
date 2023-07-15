#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-15:10:59
--------------------------------------------
"""
from flask import Blueprint
inventory = Blueprint('inventory', __name__)
from ..inventory import views