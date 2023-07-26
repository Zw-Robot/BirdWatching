#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-17:22:31
--------------------------------------------
"""
from flask import Blueprint
competition = Blueprint('competition', __name__)
from ..competiton import views