#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-15:10:59
--------------------------------------------
"""
import json
import mimetypes
import os
import uuid
from datetime import datetime
from math import ceil
from urllib.parse import quote
import pandas as pd
from flask import make_response, send_file, Response
# from pypinyin import lazy_pinyin
from sqlalchemy import or_, case, func

from apps.components.common import required_attrs_validator
from apps.inventory import inventory
from apps.models import BirdInventory, BirdSurvey, BirdRecords, BirdInfos, Userdata
from apps.components.middleware import requestPOST, login_required, requestGET, SingAuth
from apps.components.responser import Responser, FileResponser


@inventory.route('/create_bird', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def create_bird(request):
    # 鸟类名录创建接口
    username = request.json.get("username")
    order_en = request.json.get("order_en")
    order_cn = request.json.get("order_cn")
    family_en = request.json.get("family_en")
    family_cn = request.json.get("family_cn")
    genus = request.json.get("genus")
    species = request.json.get("species")
    latin_name = request.json.get("latin_name")
    geotype = request.json.get("geotype")
    seasonal = request.json.get("seasonal")
    IUCN = request.json.get("IUCN")
    level = request.json.get("level")
    describe = request.json.get("describe")
    habitat = request.json.get("habitat")
    behavior = request.json.get("behavior")
    bird_infos = request.json.get("bird_info", [])  # {"sound":[],"image":[],"video":[]}

    lost_attrs = required_attrs_validator([order_en, order_cn, family_en, family_cn, genus, species, latin_name])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    bird = BirdInventory(
        order_en=order_en,
        order_cn=order_cn,
        family_en=family_en,
        family_cn=family_cn,
        genus=genus,
        species=species,
        latin_name=latin_name,
        geotype=geotype,
        seasonal=seasonal,
        IUCN=IUCN,
        level=level,
        describe=describe,
        habitat=habitat,
        behavior=behavior,
        bird_info=json.dumps(bird_infos)
    )
    bird.update()
    return Responser.response_success(msg="创建成功")


@inventory.route('/update_bird', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def update_bird(request):
    # 鸟类记录更新接口
    username = request.json.get("username")
    bird_id = request.json.get("bird_id")
    order_en = request.json.get("order_en", "")
    order_cn = request.json.get("order_cn", "")
    family_en = request.json.get("family_en", "")
    family_cn = request.json.get("family_cn", "")
    genus = request.json.get("genus", "")
    species = request.json.get("species", "")
    latin_name = request.json.get("latin_name", "")
    geotype = request.json.get("geotype", "")
    seasonal = request.json.get("seasonal", "")
    IUCN = request.json.get("IUCN", "")
    level = request.json.get("level", "")
    describe = request.json.get("describe", "")
    habitat = request.json.get("habitat", "")
    behavior = request.json.get("behavior", "")
    bird_infos = request.json.get("bird_info", [])  # {"sound":[],"image":[],"video":[]}

    lost_attrs = required_attrs_validator([bird_id, username])
    if lost_attrs:
        return Responser.response_error('缺少参数')
    bird = BirdInventory.query.filter_by(id=bird_id).first()
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')

    bird.order_en = order_en if order_en else bird.order_en
    bird.order_cn = order_cn if order_cn else bird.order_cn
    bird.family_en = family_en if family_en else bird.family_en
    bird.family_cn = family_cn if family_cn else bird.family_cn
    bird.genus = genus if genus else bird.genus
    bird.species = species if species else bird.species
    bird.latin_name = latin_name if latin_name else bird.latin_name
    bird.geotype = geotype if geotype else bird.geotype
    bird.seasonal = seasonal if seasonal else bird.seasonal
    bird.IUCN = IUCN if IUCN else bird.IUCN
    bird.level = level if level else bird.level
    bird.describe = describe if describe else bird.describe
    bird.habitat = habitat if habitat else bird.habitat
    bird.behavior = behavior if behavior else bird.behavior
    bird.bird_info = json.dumps(bird_infos)

    bird.update()
    return Responser.response_success(msg="修改成功")


@inventory.route('/delete_bird', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def delete_bird(request):
    # 鸟类记录删除接口
    bird_id = int(request.json.get("bird_id"))

    bird = BirdInventory.query.filter_by(id=bird_id).first()
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')

    bird.is_lock = True
    bird.update()
    return Responser.response_success("删除成功")


@inventory.route('/get_all_orders', methods=["GET"])
@requestGET
def get_all_orders(request):
    bird_inventory_query = BirdInventory.query.filter_by(is_lock=False)
    result = []
    for bird in bird_inventory_query:
        if bird.order_cn[0] in [item['name'] for item in result]:
            continue
        tmp = {
            "id": len(result),
            "name": bird.order_cn[0]
        }
        result.append(tmp)
    return Responser.response_success(data=result)

# @inventory.route("/set",methods=["GET"])
# @requestGET
# def setpinying(request):
#     birds = BirdInventory.query.all()
#     for info in birds:
#         res = lazy_pinyin(info.species)
#         py = ''.join(res)
#         spy = ''
#         for n in res:
#             spy+=n[0]
#         info.pinying = py
#         info.simple_pinying = spy
#         info.update()
#     print(res)
#     return Responser.response_success()
@inventory.route('/wx_get_all_birds', methods=["GET"])
@requestGET
def wx_get_all_birds(request):
    keyword = request.args.get("keyword", "")
    order = request.args.get("order", "")
    if order:
        bird_inventory_query = BirdInventory.query.filter_by(is_lock=False).filter(
            or_(
                BirdInventory.order_cn.like(f"%{order}%")
            )
        )
    elif keyword:
        bird_inventory_query = BirdInventory.query.filter_by(is_lock=False).filter(
            or_(
                BirdInventory.family_cn.like(f"%{keyword}%"),
                BirdInventory.genus.like(f"%{keyword}%"),
                BirdInventory.order_cn.like(f"%{keyword}%"),
                BirdInventory.seasonal.like(f"%{keyword}%"),
                BirdInventory.species.like(f"%{keyword}%"),
                BirdInventory.IUCN.like(f"%{keyword}%"),
                BirdInventory.level.like(f"%{keyword}%"),
                BirdInventory.pinying.like(f"%{keyword}%"),
                BirdInventory.simple_pinying.like(f"%{keyword}%")
            )
        )
    else:
        bird_inventory_query = BirdInventory.query.filter_by(is_lock=False)
    result = []
    bird_dic = {}
    for bird in bird_inventory_query:
        bird_name = bird.order_cn + ' ' + bird.order_en
        bird_info = {
            "id": bird.id,
            'order_en': bird.order_en,
            'order_cn': bird.order_cn,
            'family_en': bird.family_en,
            'family_cn': bird.family_cn,
            'genus': bird.genus,
            'species': bird.species,
            'latin_name': bird.latin_name,
            "IUCN": bird.IUCN,
            "level": bird.level,
        }
        bird_dic[bird_name] = bird_dic.get(bird_name, [])
        bird_dic[bird_name].append(bird_info)
    for index, (key, val) in enumerate(bird_dic.items()):
        tmp_dic = {
            "id": index,
            "name": key,
            "twdata": val
        }
        result.append(tmp_dic)
    return Responser.response_success(data=result)


@inventory.route('/get_all_birds', methods=["GET"])
@requestGET
# @login_required(['sysadmin', 'admin'])
def get_all_birds(request):
    # 鸟类名录查询所有接口
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    keyword = request.args.get("keyword", "")
    order = request.args.get("order", "")
    if order:
        bird_inventory_query = BirdInventory.query.filter_by(is_lock=False).filter(
            or_(
                BirdInventory.order_cn.like(f"%{order}%")
            )
        )
    elif keyword:
        bird_inventory_query = BirdInventory.query.filter_by(is_lock=False).filter(
            or_(
                BirdInventory.family_cn.like(f"%{keyword}%"),
                BirdInventory.genus.like(f"%{keyword}%"),
                BirdInventory.order_cn.like(f"%{keyword}%"),
                BirdInventory.seasonal.like(f"%{keyword}%"),
                BirdInventory.species.like(f"%{keyword}%"),
                BirdInventory.IUCN.like(f"%{keyword}%"),
                BirdInventory.level.like(f"%{keyword}%")
            )
        )
    else:
        bird_inventory_query = BirdInventory.query.filter_by(is_lock=False)
    total_pages = ceil(bird_inventory_query.count() / per_page)

    birds = bird_inventory_query.paginate(page=page, per_page=per_page)
    result = []
    for bird in birds:
        bird_info = {
            "id": bird.id,
            'order_en': bird.order_en,
            'order_cn': bird.order_cn,
            'family_en': bird.family_en,
            'family_cn': bird.family_cn,
            'genus': bird.genus,
            'species': bird.species,
            'latin_name': bird.latin_name,
            "geotype": bird.geotype,
            "seasonal": bird.seasonal,
            "IUCN": bird.IUCN,
            "level": bird.level,
            'describe': bird.describe,
            'habitat': bird.habitat,
            'behavior': bird.behavior,
            'create_at': bird.create_at,
            'update_at': bird.update_at,
            'is_lock': bird.is_lock
        }
        result.append(bird_info)
    return Responser.response_page(data=result, count=total_pages, page=page, page_size=per_page)


@inventory.route('/get_bird', methods=["GET"])
@requestGET
# @login_required(['sysadmin', 'admin','others'])
def get_bird(request):
    # 鸟类名录查询单个接口
    bird_id = int(request.args.get('bird_id'))
    bird = BirdInventory.query.filter_by(id=bird_id).first()
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')
    files = []
    infos = bird.bird_info.split(',') if bird.bird_info else []
    for info in infos:
        temp = BirdInfos.query.get(info)
        files.append(FileResponser.get_path(temp.path if temp.path else "", temp.label))
    bird_dict = {
        'bird_id': bird.id,
        'order_en': bird.order_en,
        'order_cn': bird.order_cn,
        'family_en': bird.family_en,
        'family_cn': bird.family_cn,
        'genus': bird.genus,
        'species': bird.species,
        'latin_name': bird.latin_name,
        "geotype": bird.geotype,
        "seasonal": bird.seasonal,
        "IUCN": bird.IUCN,
        "level": bird.level,
        'describe': bird.describe,
        'habitat': bird.habitat,
        'behavior': bird.behavior,
        'bird_info': files,
        'create_at': bird.create_at,
        'update_at': bird.update_at,
    }
    return Responser.response_success(data=bird_dict)


@inventory.route('/create_bird_survey', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def create_bird_survey(request):
    # 鸟类调查创建接口
    user_id = int(request.json.get("user_id"))
    survey_name = request.json.get("survey_name", "")
    survey_desc = request.json.get("survey_desc", "")
    survey_time = request.json.get("survey_time")
    survey_location = request.json.get("survey_location", "")
    describe = request.json.get("describe", "")
    habitat = request.json.get("habitat", "")
    behavior = request.json.get("behavior", "")
    bird_infos = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([survey_name, survey_location, survey_desc, survey_time])
    if lost_attrs:
        return Responser.response_error('缺少参数')
    bird_survey = BirdSurvey(
        user_id=user_id,
        survey_name=survey_name,
        survey_desc=survey_desc,
        survey_time=datetime.strptime(survey_time, '%Y-%m-%d %H:%M:%S'),
        survey_location=survey_location,
        describe=describe,
        habitat=habitat,
        behavior=behavior,
        bird_info=json.dumps(bird_infos)
    )
    bird_survey.update()
    return Responser.response_success(msg="创建鸟类调查成功")


@inventory.route('/wx_update_bird_survey', methods=['POST'])
@requestPOST
@SingAuth
def wx_update_bird_survey(request):
    # 鸟类调查更新接口
    bird_survey_id = int(request.json.get("bird_survey_id"))
    user_id = int(request.json.get("user_id"))
    describe = request.json.get("describe", "")
    habitat = request.json.get("habitat", "")
    behavior = request.json.get("behavior", "")
    bird_infos = request.json.get("bird_info", [])
    bird_infos.appen({"user_id:user_id"})
    lost_attrs = required_attrs_validator([bird_survey_id])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    bird_survey = BirdSurvey.query.filter_by(id=bird_survey_id).first()
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')
    existing_bird_info = json.loads(bird_survey.bird_info)
    updated_bird_info = existing_bird_info + bird_infos
    bird_survey.describe = bird_survey.describe + '-' + describe if describe else bird_survey.describe
    bird_survey.habitat = bird_survey.habitat + '-' + habitat if habitat else bird_survey.habitat
    bird_survey.behavior = bird_survey.behavior + '-' + behavior if behavior else bird_survey.behavior
    bird_survey.bird_info = json.dumps(updated_bird_info)
    bird_survey.is_lock = True
    bird_survey.update()
    return Responser.response_success(msg="修改鸟类调查成功")


@inventory.route('/update_bird_survey', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def update_bird_survey(request):
    # 鸟类调查更新接口
    bird_survey_id = int(request.json.get("bird_survey_id"))
    user_id = int(request.json.get("user_id"))
    survey_name = request.json.get("survey_name", "")
    survey_desc = request.json.get("survey_desc", "")
    survey_time = request.json.get("survey_time", "")
    survey_location = request.json.get("survey_location", "")
    describe = request.json.get("describe", "")
    habitat = request.json.get("habitat", "")
    behavior = request.json.get("behavior", "")
    bird_infos = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([bird_survey_id])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    bird_survey = BirdSurvey.query.filter_by(id=bird_survey_id).first()
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')
    bird_survey.user_id = user_id if user_id else bird_survey.user_id
    bird_survey.survey_name = survey_name if survey_name else bird_survey.survey_name
    bird_survey.survey_desc = survey_desc if survey_desc else bird_survey.survey_desc
    bird_survey.survey_time = datetime.strptime(survey_time,
                                                '%Y-%m-%d %H:%M:%S') if survey_time else bird_survey.survey_time
    bird_survey.survey_location = survey_location if survey_location else bird_survey.survey_location
    bird_survey.describe = describe if describe else bird_survey.describe
    bird_survey.habitat = habitat if habitat else bird_survey.habitat
    bird_survey.behavior = behavior if behavior else bird_survey.behavior
    bird_survey.bird_info = json.dumps(bird_infos)
    bird_survey.update()
    return Responser.response_success(msg="修改鸟类调查成功")


@inventory.route('/delete_bird_survey', methods=['POST'])
@requestPOST
# @login_required(['sysadmin', 'admin'])
def delete_bird_survey(request):
    # 鸟类调查删除接口
    bird_survey_id = int(request.json.get("bird_survey_id"))

    bird_survey = BirdSurvey.query.filter_by(id=bird_survey_id).first()
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')

    bird_survey.is_lock = True
    bird_survey.update()
    return Responser.response_success("删除鸟类调查成功")


@inventory.route('/get_all_bird_surveys', methods=["GET"])
@requestGET
# @login_required(['sysadmin', 'admin'])
def get_all_bird_surveys(request):
    # 鸟类调查查询所有接口
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    bird_surveys_query = BirdSurvey.query.filter_by()

    total_pages = ceil(bird_surveys_query.count() / per_page)

    bird_surveys = bird_surveys_query.paginate(page=page, per_page=per_page)
    data = []
    for bird_survey in bird_surveys:
        user = Userdata.query.filter_by(id=int(bird_survey.user_id)).first()
        bird_survey_list = {
            'bird_survey_id': bird_survey.id,
            'user_id': user.id,
            'user_username': user.username if user else '',
            'user_name': user.name if user else '',
            'survey_name': bird_survey.survey_name,
            'survey_desc': bird_survey.survey_desc,
            'survey_time': bird_survey.survey_time,
            'survey_location': bird_survey.survey_location,
            'describe': bird_survey.describe,
            'habitat': bird_survey.habitat,
            'behavior': bird_survey.behavior,
            'bird_info': json.loads(bird_survey.bird_info),
            'create_at': bird_survey.create_at,
            'update_at': bird_survey.update_at,
            'is_lock': bird_survey.is_lock
        }
        data.append(bird_survey_list)

    return Responser.response_page(data=data, count=total_pages, page=page, page_size=per_page)


@inventory.route('/wx_get_bird_surveys', methods=["GET"])
@requestGET
# @login_required(['sysadmin', 'admin', 'others'])
def wx_get_bird_surveys(request):
    # 鸟类调查查询单个接口
    user_id = int(request.args.get("user_id", -1))
    bird_surveys = BirdSurvey.query.filter_by(user_id=user_id, is_lock=False).all()
    user = Userdata.query.filter_by(id=user_id).first()
    other = []
    if user.limit == 1:
        other = BirdSurvey.query.filter_by(user_id=8).all()

    if bird_surveys is None:
        return Responser.response_error('找不到指定的鸟类调查信息')
    data = []
    for bird_survey in bird_surveys:
        bird_survey_list = {
            'bird_survey_id': bird_survey.id,
            'survey_name': bird_survey.survey_name,
            'survey_desc': bird_survey.survey_desc,
            'survey_time': bird_survey.survey_time,
            'survey_location': bird_survey.survey_location,
            'is_lock': bird_survey.is_lock
        }
        data.append(bird_survey_list)
    for bird_survey in other:
        bird_survey_list = {
            'bird_survey_id': bird_survey.id,
            'survey_name': bird_survey.survey_name,
            'survey_desc': bird_survey.survey_desc,
            'survey_time': bird_survey.survey_time,
            'survey_location': bird_survey.survey_location,
            'is_lock': bird_survey.is_lock
        }
        data.append(bird_survey_list)

    return Responser.response_success(data=data)


@inventory.route('/wx_get_survey', methods=["GET"])
@requestGET
# @login_required(['sysadmin', 'admin', 'others'])
def wx_get_survey(request):
    # 鸟类调查查询单个接口
    survey_id = int(request.args.get("survey_id", -1))
    bird_survey = BirdSurvey.query.filter_by(id=survey_id).first()
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')
    bird_survey_d = {
        'survey_name': bird_survey.survey_name,
        'survey_desc': bird_survey.survey_desc,
        'survey_time': bird_survey.survey_time,
        'survey_location': bird_survey.survey_location,
        'describe': bird_survey.describe,
        'habitat': bird_survey.habitat,
        'behavior': bird_survey.behavior,
        'bird_info': json.loads(bird_survey.bird_info),
        'create_at': bird_survey.create_at,
        'update_at': bird_survey.update_at,
        'is_lock': bird_survey.is_lock
    }

    return Responser.response_success(data=bird_survey_d)


# @inventory.route('/update_bird_record', methods=['POST'])
# @requestPOST
# # @login_required(['sysadmin', 'admin', 'others'])
# def update_bird_record(request):
#     # 鸟类记录更新接口
#     bird_record_id = request.json.get("bird_record_id")
#     user_id = request.json.get("user_id")
#     bird_id = request.json.get("bird_id")
#     record_time = request.json.get("record_time", "")
#     longitude = request.json.get("longitude", "")
#     latitude = request.json.get("latitude", "")
#     weather = request.json.get("weather", "")
#     temperature = request.json.get("temperature", "")
#     record_location = request.json.get("record_location", "")
#     record_describe = request.json.get("record_describe", "")
#     bird_infos = request.json.get("bird_info", [])
#
#     lost_attrs = required_attrs_validator([user_id, bird_id, bird_record_id])
#     if lost_attrs:
#         return Responser.response_error('缺少参数')
#
#     bird_record = BirdRecords.query.get(bird_record_id)
#     if bird_record is None:
#         return Responser.response_error('找不到指定的鸟类记录')
#     if bird_record.user_id != user_id:
#         return Responser.response_error('没有权限修改该鸟类记录')
#
#     bird_record.bird_id = bird_id if bird_id else bird_record.bird_id
#     bird_record.record_time = record_time if record_time else bird_record.record_time
#     bird_record.record_location = record_location if record_location else bird_record.record_location
#     bird_record.record_describe = record_describe if record_describe else bird_record.record_describe
#     bird_record.longitude = longitude if longitude else bird_record.longitude
#     bird_record.latitude = latitude if latitude else bird_record.latitude
#     bird_record.weather = weather if weather else bird_record.weather
#     bird_record.temperature = temperature if temperature else bird_record.temperature
#     bird_record.bird_info = json.dumps(bird_infos)
#     bird_record.update()
#     return Responser.response_success(msg="修改鸟类记录成功")


@inventory.route('/delete_bird_record', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def delete_bird_record(request):
    # 鸟类记录删除接口
    bird_record_id = int(request.args.get("record_id"))

    bird_record = BirdRecords.query.filter_by(id=bird_record_id).first()
    if bird_record is None:
        return Responser.response_error('找不到指定的鸟类记录')

    bird_record.is_lock = True
    bird_record.update()
    return Responser.response_success("删除鸟类记录成功")


@inventory.route('/get_all_bird_records', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin'])
def get_all_bird_records(request):
    # 鸟类记录获取所有接口

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    bird_records_query = BirdRecords.query.filter_by(is_lock=False)

    total_pages = ceil(bird_records_query.count() / per_page)

    bird_records = bird_records_query.paginate(page=page, per_page=per_page)

    bird_record_list = []
    for bird_record in bird_records:
        bird_record_dict = {
            'bird_record_id': bird_record.id,
            'user_id': bird_record.user_id,
            'bird_id': bird_record.bird_id,
            'record_time': bird_record.record_time,
            'record_location': bird_record.record_location,
            'record_describe': bird_record.record_describe,
            "longitude": bird_record.longitude,
            "latitude": bird_record.latitude,
            "weather": bird_record.weather,
            "temperature": bird_record.temperature,
            'bird_info': json.loads(bird_record.bird_info),
            'create_at': bird_record.create_at,
            'update_at': bird_record.update_at,
            'is_lock': bird_record.is_lock
        }
        bird_record_list.append(bird_record_dict)
    return Responser.response_page(data=bird_record_list, count=total_pages, page=page, page_size=per_page)


@inventory.route('/get_bird_record', methods=["GET"])
@requestGET
def get_bird_record(request):
    # 鸟类记录获取单个接口
    bird_record_id = int(request.args.get("bird_record_id"))
    bird_record = BirdRecords.query.get(bird_record_id)
    if bird_record is None:
        return Responser.response_error('找不到指定的鸟类记录')
    files = []
    infos = bird_record.bird_info.split(',') if bird_record.bird_info else []
    for info in infos:
        temp = BirdInfos.query.get(info)
        files.append(FileResponser.get_path(temp.path if temp.path else "", temp.label))
    bird_record_dict = {
        'bird_record_id': bird_record.id,
        'user_id': bird_record.user_id,
        'bird_id': bird_record.bird_id,
        'record_time': bird_record.record_time,
        'record_location': bird_record.record_location,
        'record_describe': bird_record.record_describe,
        "longitude": bird_record.longitude,
        "latitude": bird_record.latitude,
        "weather": bird_record.weather,
        "temperature": bird_record.temperature,
        'bird_info': infos,
        'create_at': bird_record.create_at,
        'update_at': bird_record.update_at,
    }
    return Responser.response_success(data=bird_record_dict)


@inventory.route('/wx_get_record', methods=["GET"])
@requestGET
def wx_get_record(request):
    userid = int(request.args.get("user_id"))
    record = int(request.args.get("recordid", '-1'))
    print(record)
    if record > 0:
        bird_records = BirdRecords.query.filter_by(id=record, user_id=userid, is_lock=False).all()
    else:
        bird_records = BirdRecords.query.filter_by(user_id=userid, is_lock=False).all()
    rec = []
    for bird_record in bird_records:
        bi = BirdInventory.query.filter_by(id=bird_record.bird_id).first()
        bird_record_dict = {
            'id': bird_record.id,
            'bird': bi.species if bi else '',
            'order_en': bi.order_en if bi else bi,
            'order_cn': bi.order_cn if bi else bi,
            'family_en': bi.family_en if bi else bi,
            'family_cn': bi.family_cn if bi else bi,
            'genus': bi.genus if bi else bi,
            'species': bi.species if bi else bi,
            'latin_name': bi.latin_name if bi else bi,
            "geotype": bi.geotype if bi else bi,
            "seasonal": bi.seasonal if bi else bi,
            "IUCN": bi.IUCN if bi else '',
            "level": bi.level if bi else '',
            'record_time': bird_record.record_time,
            'record_location': bird_record.record_location,
            'record_describe': bird_record.record_describe,
            "longitude": bird_record.longitude,
            "latitude": bird_record.latitude,
            "weather": bird_record.weather,
            "temperature": bird_record.temperature,
            'bird_info': json.loads(bird_record.bird_info),
            'create_at': bird_record.create_at,
            'update_at': bird_record.update_at,
        }
        rec.append(bird_record_dict)
    return Responser.response_success(data=rec)


@inventory.route('/wx_create_bird_record', methods=['POST'])
@requestPOST
@SingAuth
def wx_create_bird_record(request):
    # 鸟类记录创建接口
    user_id = request.json.get("user_id")
    user = Userdata.query.filter_by(id=user_id).first()
    if user:
        user.score = user.score + 1
    else:
        return Responser.response_error("没有该用户！")
    bird_id = int(request.json.get("recordid", '-1'))
    record_time = request.json.get("record_time")
    record_location = request.json.get("record_location")
    longitude = request.json.get("longitude")
    latitude = request.json.get("latitude")
    weather = request.json.get("weather")
    temperature = request.json.get("temperature")
    record_describe = request.json.get("record_describe")
    bird_infos = request.json.get("bird_infos", [])
    print(bird_infos)
    # lost_attrs = required_attrs_validator([bird_id, record_time, record_location])
    # if lost_attrs:
    #     return Responser.response_error('缺少参数')

    bird_record = BirdRecords(
        user_id=user_id,
        bird_id=bird_id,
        record_time=record_time,
        record_location=record_location,
        record_describe=record_describe,
        longitude=longitude,
        latitude=latitude,
        weather=weather,
        temperature=temperature,
        bird_info=json.dumps(bird_infos)
    )
    bird_record.update()
    return Responser.response_success(msg="创建鸟类记录成功")


@inventory.route('/get_file/<filename>', methods=["GET"])
@requestGET
def get_images_value(request, filename):
    path = "/robot/birdwatching/var/{}".format(filename)
    if os.path.exists(path):
        mimetype, _ = mimetypes.guess_type(path)
        return send_file(path, mimetype=mimetype, as_attachment=False)
    else:
        return Responser.response_error("error没有文件")


@inventory.route('/get_show_images', methods=["GET"])
@requestGET
def get_show_images(request):
    path = "/robot/birdwatching/show/"
    li = os.listdir(path)
    return Responser.response_success(data=li)


@inventory.route('/wx_post_base64', methods=["POST"])
@requestPOST
def wx_post_base64(request):
    type = request.json.get("type")
    binary = request.json.get("binary")
    print(type)
    if type == "sound":
        path = FileResponser.audio_save(binary)
    elif type == "image":
        path = FileResponser.image_save(binary)
    elif type == "video":
        path = FileResponser.video_save(binary)
    else:
        path = ""
    return Responser.response_success(data={"data": path})


@inventory.route('/wx_delete_bird_record', methods=['POST'])
@requestPOST
@SingAuth
def wx_delete_bird_record(request):
    # 鸟类记录删除接口
    bird_record_id = int(request.json.get("record_id"))

    bird_record = BirdRecords.query.filter_by(id=bird_record_id).first()
    if bird_record is None:
        return Responser.response_error('找不到指定的鸟类记录')

    bird_record.is_lock = True
    bird_record.update()
    return Responser.response_success("删除鸟类记录成功")


@inventory.route('/download_records', methods=['POST'])
@requestPOST
def download_record(request):
    # 查询所有鸟类记录
    select_records = request.json.get("select_records")
    records_list = [int(id) for id in select_records.split(",")]
    if select_records:
        bird_records = BirdRecords.query.filter(BirdRecords.id.in_(records_list)).all()
    else:
        bird_records = BirdRecords.query.all()

    record = []
    for bird_record in bird_records:
        bi = BirdInventory.query.filter_by(id=bird_record.id).first()
        bird_record_dict = {
            'id': bird_record.id,
            'bird': bi.species if bi else '',
            'record_time': bird_record.record_time,
            'record_location': bird_record.record_location,
            'record_describe': bird_record.record_describe,
            "longitude": bird_record.longitude,
            "latitude": bird_record.latitude,
            "weather": bird_record.weather,
            "temperature": bird_record.temperature,
            'bird_info': json.loads(bird_record.bird_info),
            'create_at': bird_record.create_at,
            'update_at': bird_record.update_at,
        }
        record.append(bird_record_dict)
    # 将查询结果转换为DataFrame
    df = pd.DataFrame(record)

    # 将DataFrame保存为Excel文件
    excel_file = '/robot/birdwatching/var/bird_records.xlsx'  # 替换为您想要保存的文件名
    df.to_excel(excel_file, index=False)

    # 设置响应头部的内容类型和文件名
    results = open('/robot/birdwatching/var/bird_records.xlsx', 'rb').read()
    return Response(results, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    headers={"Content-Disposition": 'attachment; filename=bird_records.xlsx'})


@inventory.route("/download_example_bird", methods=["POST"])
@requestPOST
def download_example_bird(request):
    if os.path.exists('/robot/birdwatching/var/example_bird.xlsx'):
        os.remove('/robot/birdwatching/var/example_bird.xlsx')
    bird_dic = {
        "order_en": '目 英文',
        "order_cn": '目 中文',
        "family_en": '科 英文',
        "family_cn": '科 中文',
        "genus": '属',
        "species": '种',
        "latin_name": '拉丁名',
        "geotype": '地理属性',
        "seasonal": '季节属性',
        "IUCN": 'IUCN',
        "level": '保护等级',
        "describe": '描述',
        "habitat": '生境',
        "behavior": '习性',
        "bird_info": '其他'
    }
    df = pd.DataFrame([bird_dic])
    df.to_excel('./example_bird.xlsx', index=False)
    # response = make_response(send_file('/robot/birdwatching/var/example_bird.xlsx', as_attachment=True))
    # response.headers['Content-Disposition'] = 'attachment; filename=exported_records.xlsx'
    # response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    # return response

    results = open('./example_bird.xlsx', 'rb').read()
    return Response(results, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    headers={"Content-Disposition": 'attachment; filename=example_bird.xlsx'})


@inventory.route("/upload_bird", methods=["POST"])
@requestPOST
def upload_file(request):
    excel_file = request.files['excelFile']
    df = pd.read_excel(excel_file)
    print(df)
    desired_columns = [
        "order_en",
        "order_cn",
        "family_en",
        "family_cn",
        "genus",
        "species",
        "latin_name",
        "geotype",
        "seasonal",
        "IUCN",
        "level",
        "describe",
        "habitat",
        "behavior",
        "bird_info"
    ]
    # 获取数据框的列名，并转换为集合
    columns_set = set(df.columns)
    if set(desired_columns).issubset(columns_set):
        print("All desired columns are present.")
    else:
        return Responser.response_error("格式不对，请根据格式上传")

    for index, row in df.iterrows():
        bird = BirdInventory(
            order_en=row['order_en'] if row['order_en'] else '',
            order_cn=row['order_cn'] if row['order_cn'] else '',
            family_en=row['family_en'] if row['family_en'] else '',
            family_cn=row['family_cn'] if row['family_cn'] else '',
            genus=row['genus'] if row['genus'] else '',
            species=row['species'] if row['species'] else '',
            latin_name=row['latin_name'] if row['latin_name'] else '',
            geotype=row['geotype'] if row['geotype'] else '',
            seasonal=row['seasonal'] if row['seasonal'] else '',
            IUCN=row['IUCN'] if row['IUCN'] else '',
            level=row['level'] if row['level'] else '',
            describe=row['describe'] if row['describe'] else '',
            habitat=row['habitat'] if row['habitat'] else '',
            behavior=row['behavior'] if row['behavior'] else '',
            bird_info=row['bird_info'] if row['bird_info'] else '',
        )
        bird.update()
    # 判断所需的表头是否存在

    return Responser.response_success(msg="上传成功！")
