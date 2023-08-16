#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-17:22:32
--------------------------------------------
"""
import math

from flask import request
from login import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

from apps.competiton import competition
from apps.components.middleware import requestPOST, login_required, requestGET
from apps.components.responser import Responser
from apps.models import BirdMatch, MatchGroup


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
@login_required(['sysadmin', 'admin', 'other'])
def get_all_matches(request):
    #获取鸟类所有比赛
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    bird_matches_query = BirdMatch.query.filter_by(is_lock=False)

    total_pages = math.ceil(bird_matches_query.count() / per_page)

    bird_matches_paginated = bird_matches_query.paginate(page=page, per_page=per_page, error_out=False)

    match_list = []
    for bird_match in bird_matches_paginated.items:
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

    pagination_data = {
        'current_page': bird_matches_paginated.page,
        'total_pages': total_pages,
        'total_items': bird_matches_paginated.total,
        'per_page': per_page
    }

    return Responser.response_success(data=match_list, pagination=pagination_data)


@competition.route('/create_group', methods=['POST'])
@requestPOST
@login_required(['sysadmin'])
def create_group(request, db_session=None):
    # 比赛小组创建接口
    match_id = request.json.get("match_id")
    group_name = request.json.get("group_name")
    group_desc = request.json.get("group_desc")
    group_user = request.json.get("group_user")
    password = request.json.get("password")
    hashed_password = generate_password_hash(password)

    group = MatchGroup(match_id=match_id, group_name=group_name, group_desc=group_desc, group_user=group_user, password=hashed_password)
    try:
        db_session.add(group)
        db_session.commit()
        return Responser.response_success(msg="小组创建成功"), 201
    except SQLAlchemyError as e:
        db_session.rollback()
        return Responser.response_error(str(e)), 500

@competition.route('/update_group', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'other'])
def update_group(request, db_session=None):
    # 比赛小组更新接口
    group_id = request.json.get("group_id")
    group_name = request.json.get("group_name")
    group_desc = request.json.get("group_desc")
    group_user = request.json.get("group_user")

    group = MatchGroup.query.get(group_id)
    if group is None:
        return Responser.response_error('找不到指定的小组信息'), 404

    group.group_name = group_name
    group.group_desc = group_desc
    group.group_user = group_user

    try:
        db_session.commit()
        return Responser.response_success(msg="小组信息更新成功"), 200
    except SQLAlchemyError as e:
        db_session.rollback()
        return Responser.response_error(str(e)), 500

@competition.route('/delete_group', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def delete_group(request, db_session=None):
    # 比赛小组删除接口
    group_id = request.json.get("group_id")

    group = MatchGroup.query.get(group_id)
    if group is None:
        return Responser.response_error('找不到指定的小组信息'), 404

    try:
        db_session.delete(group)
        db_session.commit()
        return Responser.response_success(msg="小组删除成功"), 200
    except SQLAlchemyError as e:
        db_session.rollback()
        return Responser.response_error(str(e)), 500

@competition.route('/get_all_groups', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin', 'other'])
def get_all_groups(request):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    groups_query = MatchGroup.query

    total_pages = math.ceil(groups_query.count() / per_page)

    groups_paginated = groups_query.paginate(page=page, per_page=per_page, error_out=False)

    group_list = []
    for group in groups_paginated.items:
        group_dict = {
            'group_id': group.id,
            'match_id': group.match_id,
            'group_name': group.group_name,
            'group_desc': group.group_desc,
            'group_user': group.group_user,
            'rank': group.rank,
            'create_at': group.create_at,
            'update_at': group.update_at
        }
        group_list.append(group_dict)

    pagination_data = {
        'current_page': groups_paginated.page,
        'total_pages': total_pages,
        'total_items': groups_paginated.total,
        'per_page': per_page
    }

    return Responser.response_success(data=group_list, pagination=pagination_data)
