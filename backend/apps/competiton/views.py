#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-17:22:32
--------------------------------------------
"""
from flask import request

from apps.competiton import competition
from apps.components.middleware import requestPOST, login_required, requestGET
from apps.components.responser import Responser
from apps.models import BirdMatch

@competition.route('/create_match', methods=['POST'])
@requestPOST
@login_required(['sysadmin'])
def create_match(request):
    # 鸟类比赛创建接口
    match_create = request.json.get("match_create")
    match_name = request.json.get("match_name")
    match_desc = request.json.get("match_desc")
    match_location = request.json.get("match_location")
    referee = request.json.get("referee")
    match_image = request.json.get("match_image")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")

    required_attrs = [match_create, match_name, match_location, referee, start_time, end_time]
    if any(attr is None for attr in required_attrs):
        return Responser.response_error('缺少必要参数')

    bird_match = BirdMatch(
        match_create=match_create,
        match_name=match_name,
        match_desc=match_desc,
        match_location=match_location,
        referee=referee,
        match_image=match_image,
        start_time=start_time,
        end_time=end_time
    )
    bird_match.update()
    return Responser.response_success(msg="比赛创建成功")

@competition.route('/update_match', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin','other'])
def update_match(request):
    # 鸟类比赛更新接口
    match_id = request.json.get("match_id")
    match_create = request.json.get("match_create")
    match_name = request.json.get("match_name")
    match_desc = request.json.get("match_desc")
    match_location = request.json.get("match_location")
    referee = request.json.get("referee")
    match_image = request.json.get("match_image")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")


    required_attrs = [match_id, match_create, match_name, match_location, referee, start_time, end_time]
    if any(attr is None for attr in required_attrs):
        return Responser.response_error('缺少必要参数')

    bird_match = BirdMatch.query.get(match_id)
    if bird_match is None:
        return Responser.response_error('找不到指定的比赛信息')

    bird_match.match_create = match_create
    bird_match.match_name = match_name
    bird_match.match_desc = match_desc
    bird_match.match_location = match_location
    bird_match.referee = referee
    bird_match.match_image = match_image
    bird_match.start_time = start_time
    bird_match.end_time = end_time

    bird_match.update()
    return Responser.response_success(msg="比赛信息更新成功")


@competition.route('/delete_match', methods=['GET'])
@requestGET
@login_required(['sysadmin', 'admin'])
def delete_match(request):
    # 鸟类比赛删除接口
    match_id = request.json.get("match_id")

    bird_match = BirdMatch.query.get(match_id)
    if bird_match is None:
        return Responser.response_error('找不到指定的比赛信息')

    bird_match.is_lock = True
    bird_match.update()
    return Responser.response_success("比赛删除成功")

@competition.route('/get_all_matches', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin','other'])
def get_all_matches(request):
    # 查询所有未删除的比赛信息
    bird_matches = BirdMatch.query.filter_by(is_lock=False).all()
    match_list = []

    for bird_match in bird_matches:
        match_dict = {
            'match_id': bird_match.id,
            'match_create': bird_match.match_create,
            'match_name': bird_match.match_name,
            'match_desc': bird_match.match_desc,
            'match_location': bird_match.match_location,
            'referee': bird_match.referee,
            'match_image': bird_match.match_image,
            'start_time': bird_match.start_time,
            'end_time': bird_match.end_time,
            'create_at': bird_match.create_at,
            'update_at': bird_match.update_at
        }
        match_list.append(match_dict)

    return Responser.response_success(data=match_list)
