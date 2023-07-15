#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-15:10:59
--------------------------------------------
"""
from flask import Blueprint, request
from apps.components.common import required_attrs_validator
from apps.models import BirdInventory, BirdImageSound
from apps.components.middleware import requestPOST, login_required, requestGET
from apps.components.responser import Responser

inventory = Blueprint('inventory', __name__)

@inventory.route('/create_bird', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def create_bird(request):
    order_en = request.json.get("order_en")
    order_cn = request.json.get("order_cn")
    family_en = request.json.get("family_en")
    family_cn = request.json.get("family_cn")
    genus = request.json.get("genus")
    species = request.json.get("species")
    latin_name = request.json.get("latin_name")
    describe = request.json.get("describe")
    habitat = request.json.get("habitat")
    behavior = request.json.get("behavior")
    bird_info_ids = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([order_en, order_cn, family_en, family_cn, genus, species, latin_name])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    invalid_bird_info_ids = []
    for bird_info_id in bird_info_ids:
        bird_info = BirdImageSound.query.get(bird_info_id)
        if bird_info is None:
            invalid_bird_info_ids.append(bird_info_id)
    if invalid_bird_info_ids:
        return Responser.response_error('无效的鸟类声音图像信息ID: {}'.format(invalid_bird_info_ids))

    bird = BirdInventory(
        order_en=order_en,
        order_cn=order_cn,
        family_en=family_en,
        family_cn=family_cn,
        genus=genus,
        species=species,
        latin_name=latin_name,
        describe=describe,
        habitat=habitat,
        behavior=behavior,
        bird_info=','.join(map(str, bird_info_ids))
    )
    bird.update()
    return Responser.response_success(msg="创建成功")

@inventory.route('/update_bird', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin','others'])
def update_bird(request):
    bird_id = request.json.get("bird_id")
    order_en = request.json.get("order_en")
    order_cn = request.json.get("order_cn")
    family_en = request.json.get("family_en")
    family_cn = request.json.get("family_cn")
    genus = request.json.get("genus")
    species = request.json.get("species")
    latin_name = request.json.get("latin_name")
    describe = request.json.get("describe")
    habitat = request.json.get("habitat")
    behavior = request.json.get("behavior")
    bird_info_ids = request.json.get("bird_info", [])

    bird = BirdInventory.query.get(bird_id)
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')
    lost_attrs = required_attrs_validator([order_en, order_cn, family_en, family_cn, genus, species, latin_name])
    if lost_attrs:
        return Responser.response_error('缺少参数')
    invalid_bird_info_ids = []
    for bird_info_id in bird_info_ids:
        bird_info = BirdImageSound.query.get(bird_info_id)
        if bird_info is None:
            invalid_bird_info_ids.append(bird_info_id)
    if invalid_bird_info_ids:
        return Responser.response_error('无效的鸟类声音图像信息ID: {}'.format(invalid_bird_info_ids))
    bird.order_en = order_en
    bird.order_cn = order_cn
    bird.family_en = family_en
    bird.family_cn = family_cn
    bird.genus = genus
    bird.species = species
    bird.latin_name = latin_name
    bird.describe = describe
    bird.habitat = habitat
    bird.behavior = behavior
    bird.bird_info = ','.join(map(str, bird_info_ids))
    bird.update()
    return Responser.response_success(msg="修改成功")

@inventory.route('/delete_bird', methods=['GET'])
@requestGET
@login_required(['sysadmin'])
def delete_bird(request):
    bird_id = request.json.get("bird_id")

    bird = BirdInventory.query.get(bird_id)
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')

    bird.is_lock = True
    bird.update()
    return Responser.response_success("删除成功")

@inventory.route('/get_all_birds', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin','others'])
def get_all_birds():
    birds = BirdInventory.query.filter_by().all()
    bird_list = []
    for bird in birds:
        bird_dict = {
            'bird_id': bird.id,
            'order_en': bird.order_en,
            'order_cn': bird.order_cn,
            'family_en': bird.family_en,
            'family_cn': bird.family_cn,
            'genus': bird.genus,
            'species': bird.species,
            'latin_name': bird.latin_name,
            'describe': bird.describe,
            'habitat': bird.habitat,
            'behavior': bird.behavior,
            'bird_info': bird.bird_info.split(',') if bird.bird_info else [],
            'create_at': bird.create_at,
            'update_at': bird.update_at,
            'is_lock': bird.is_lock
        }
        bird_list.append(bird_dict)
    return Responser.response_success(data=bird_list)

@inventory.route('/get_bird', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin','others'])
def get_bird(request):
    bird_id = request.json.get("bird_id")
    bird = BirdInventory.query.get(bird_id)
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')
    bird_dict = {
        'bird_id': bird.id,
        'order_en': bird.order_en,
        'order_cn': bird.order_cn,
        'family_en': bird.family_en,
        'family_cn': bird.family_cn,
        'genus': bird.genus,
        'species': bird.species,
        'latin_name': bird.latin_name,
        'describe': bird.describe,
        'habitat': bird.habitat,
        'behavior': bird.behavior,
        'bird_info': bird.bird_info.split(',') if bird.bird_info else [],
        'create_at': bird.create_at,
        'update_at': bird.update_at,
    }
    return Responser.response_success(data=bird_dict)
