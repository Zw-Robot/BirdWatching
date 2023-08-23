#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-17:22:32
--------------------------------------------
"""
import math

from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from apps.competition import competition
from apps.components.middleware import requestPOST, requestGET, SingAuth, login_required
from apps.components.responser import Responser
from apps.models import BirdMatch, MatchGroup, Userdata


@competition.route('/create_match', methods=['POST'])
@requestPOST
# @login_required(['sysadmin'])
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
# @login_required(['sysadmin', 'admin', 'other'])
def update_match(request):
    # 鸟类比赛更新接口
    match_id = int(request.json.get("match_id"))
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

    bird_match = BirdMatch.query.filter_by(match_id).first()
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
    match_id = int(request.args.get("match_id"))

    bird_match = BirdMatch.query.filter_by(match_id).first()
    if bird_match is None:
        return Responser.response_error('找不到指定的比赛信息')

    bird_match.is_lock = True
    bird_match.update()
    return Responser.response_success("比赛删除成功")


@competition.route('/get_all_matches', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin', 'other'])
def get_all_matches(request):
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

    return Responser.response_page(data=match_list,page=page,page_size=per_page,count=total_pages)


@competition.route('/create_group', methods=['POST'])
@requestPOST
@SingAuth
def create_group(request):
    # 比赛小组创建接口
    match_id = int(request.json.get("match_id"))
    group_name = request.json.get("group_name")
    group_desc = request.json.get("group_desc")
    group_user = str(request.json.get("user_id"))
    password = request.json.get("password")
    bmatch = BirdMatch.query.filter_by(id=match_id)
    if not bmatch:
        return Responser.response_error(msg="创建失败")
    group = MatchGroup.query.filter_by(group_name=group_name).first()
    if group:
        return Responser.response_error(msg="已存在该小组")

    group_user = ','.join(map(str, group_user))
    group = MatchGroup(match_id=match_id, group_name=group_name, hash_password=password, group_desc=group_desc,
                       group_user=group_user,
                       )
    group.update()
    return Responser.response_success(msg="小组创建成功")


@competition.route('/update_group', methods=['POST'])
@requestPOST
def update_group(request, db_session=None):
    # 比赛小组更新接口
    group_id = request.json.get("group_id")
    group_name = request.json.get("group_name")
    group_desc = request.json.get("group_desc")
    group_user = request.json.get("group_user")
    group_rank = request.json.get("group_rank")
    group_user = ','.join(map(str, group_user))

    group = MatchGroup.query.get(group_id)
    if group is None:
        return Responser.response_error('找不到指定的小组信息')

    group.group_name = group_name
    group.group_desc = group_desc
    group.group_user = group_user
    group.rank = group_rank
    group.update()
    return Responser.response_success(msg="小组信息更新成功")


@competition.route('/delete_group', methods=['POST'])
@requestPOST
@SingAuth
def delete_group(request):
    # 比赛小组删除接口
    group_id = request.json.get("group_id")

    group = MatchGroup.query.get(group_id)
    if group is None:
        return Responser.response_error('找不到指定的小组信息')

    group.is_lock = True
    group.update()
    return Responser.response_success(msg="小组删除成功")


@competition.route('/add_group', methods=["POST"])
@requestPOST
@SingAuth
def add_group(request):
    group_name = request.json.get("group_name")
    group_user = str(request.json.get("user_id"))
    password = request.json.get("password")
    group = MatchGroup.query.filter_by(group_name=group_name).first()
    if group is None:
        return Responser.response_error('找不到指定的小组信息')
    if group.check_password(password):
        return Responser.response_error('密码错误')
    if group_user in group.group_user:
        return Responser.response_error(msg="已加入该小组")
    group.group_user = group.group_user + ',' + group_user
    group.update()
    return Responser.response_success(msg="加入小组成功")

# 退出group
@competition.route('/exit_group', methods=["POST"])
@requestPOST
@SingAuth
def exit_group(request):
    user_id = str(request.json.get("user_id"))
    group = MatchGroup.query.filter_by(is_lock=False).filter(
        or_(
            MatchGroup.group_user.like(f"%{user_id}%")
        )
    ).first()
    if group is None:
        return Responser.response_error('找不到指定的小组信息')
    group_user = group.group_user.split(',')
    print(group_user)
    group_user.remove(user_id)
    group.group_user = ",".join(map(str,group_user))
    group.update()
    return Responser.response_success(data={},msg="退出小组成功")


# 组别
@competition.route('/wx_user_group', methods=["GET"])
@requestGET
def wx_user_group(request):
    user_id = int(request.args.get("user_id"))
    groups = MatchGroup.query.filter_by(is_lock=False).filter(
        or_(
            MatchGroup.group_user.like(f"%{user_id}%")
        )
    )
    res = []
    for group in groups:
        match = BirdMatch.query.filter_by(id=group.match_id).first()
        users = group.group_user
        gnames = []
        names = users.split(',')
        print(names)
        for name in names:
            gtemp = Userdata.query.filter_by(id = int(name)).first()
            if gtemp:
                gnames.append(gtemp.username)
        dic = {
            'group_id': group.id,
            'match_id': match.id,
            'match_name': match.match_name,
            'match_desc': match.match_desc,
            'group_name': group.group_name,
            'group_desc': group.group_desc,
            'group_user': gnames,
            'rank': group.rank,
            'create_at': group.create_at,
            'update_at': group.update_at
        }
        res.append(dic)
    return Responser.response_success(data={"data":res})


@competition.route('/get_all_groups', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin', 'other'])
def get_all_groups(request):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    match_id = int(request.args.get('match_id',1))

    groups_query = MatchGroup.query.filter_by(match_id=match_id)
    total_pages = math.ceil(groups_query.count() / per_page)

    groups_paginated = groups_query.paginate(page=page, per_page=per_page, error_out=False)

    group_list = []
    for group in groups_paginated:
        match = BirdMatch.query.filter_by(id=group.match_id).first()
        users = group.group_user
        gnames = []
        names = users.split(',')
        print(names)
        for name in names:
            gtemp = Userdata.query.filter_by(id=int(name)).first()
            if gtemp:
                gnames.append(gtemp.username)
        dic = {
            'group_id': group.id,
            'match_id': match.id,
            'match_name': match.match_name,
            'match_desc': match.match_desc,
            'group_name': group.group_name,
            'group_desc': group.group_desc,
            'group_user': gnames,
            'rank': group.rank,
            'create_at': group.create_at,
            'update_at': group.update_at
        }
        group_list.append(dic)


    return Responser.response_page(data=group_list,page=page,page_size=per_page,count=total_pages)