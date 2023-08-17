#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-15:10:59
--------------------------------------------
"""
from datetime import datetime

from flask import Blueprint, request, Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy

from apps.components.common import required_attrs_validator
from apps.models import BirdInventory, BirdInfos, BirdSurvey, BirdRecords
from apps.components.middleware import requestPOST, login_required, requestGET
from apps.components.responser import Responser, FileResponser

inventory = Blueprint('inventory', __name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bird_inventory.db'
db = SQLAlchemy(app)


@inventory.route('/import_bird_inventory', methods=['POST'])
@requestPOST
@login_required(['sysadmin'])
def import_bird_inventory():
    try:
        data = request.json
        order_en = data.get("order_en")
        order_cn = data.get("order_cn")
        family_en = data.get("family_en")
        family_cn = data.get("family_cn")
        genus = data.get("genus")
        species = data.get("species")
        latin_name = data.get("latin_name")
        geotype = data.get("geotype")
        seasonal = data.get("seasonal")
        IUCN = data.get("IUCN")
        level = data.get("level")
        describe = data.get("describe")
        habitat = data.get("habitat")
        behavior = data.get("behavior")
        bird_info_ids = data.get("bird_info", [])

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
            bird_info=','.join(map(str, bird_info_ids))
        )

        db.session.add(bird)
        db.session.commit()

        return jsonify({"message": "成功导入鸟库信息。"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    @inventory.route('/export_bird_records', methods=['GET'])
    @requestPOST
    @login_required(['sysadmin'])
    def export_bird_records():
        try:
            bird_records = BirdRecords.query.all()

            records_data = []
            for record in bird_records:
                record_data = {
                    "user_id": record.user_id,
                    "bird_id": record.bird_id,
                    "record_time": record.record_time,
                    "record_location": record.record_location,
                    "longitude": record.longitude,
                    "latitude": record.latitude,
                    "weather": record.weather,
                    "temperature": record.temperature,
                    "record_describe": record.record_describe,
                    "bird_info": record.bird_info,
                }
                records_data.append(record_data)

            return jsonify({"bird_records": records_data}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@inventory.route('/create_bird', methods=['POST'])
@requestPOST
@login_required(['sysadmin'])
def create_bird(request):
    # 鸟类名录创建接口
    order_en = request.json.get("order_en")
    order_cn = request.json.get("order_cn")
    family_en = request.json.get("family_en")
    family_cn = request.json.get("family_cn")
    genus = request.json.get("genus")
    species = request.json.get("species")
    latin_name = request.json.get("latin_name")
    geotype = request.json.get("geotype")  # 添加地理型字段
    seasonal = request.json.get("seasonal")  # 添加季节型字段
    IUCN = request.json.get("IUCN")  # 添加濒危等级字段
    level = request.json.get("level")  # 添加保护等级字段
    describe = request.json.get("describe")
    habitat = request.json.get("habitat")
    behavior = request.json.get("behavior")
    bird_info_ids = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([order_en, order_cn, family_en, family_cn, genus, species, latin_name])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    invalid_bird_info_ids = []
    for bird_info_id in bird_info_ids:
        bird_info = bird_info.query.get(bird_info_id)
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
        geotype=geotype,
        seasonal=seasonal,
        IUCN=IUCN,
        level=level,
        describe=describe,
        habitat=habitat,
        behavior=behavior,
        bird_info=','.join(map(str, bird_info_ids))
    )
    bird.update()
    return Responser.response_success(msg="创建成功")

@inventory.route('/update_bird', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def update_bird(request):
    # 鸟类名录更新接口
    bird_id = request.json.get("bird_id")
    order_en = request.json.get("order_en")
    order_cn = request.json.get("order_cn")
    family_en = request.json.get("family_en")
    family_cn = request.json.get("family_cn")
    genus = request.json.get("genus")
    species = request.json.get("species")
    latin_name = request.json.get("latin_name")
    geotype = request.json.get("geotype")  # 添加地理型字段
    seasonal = request.json.get("seasonal")  # 添加季节型字段
    IUCN = request.json.get("IUCN")  # 添加濒危等级字段
    level = request.json.get("level")  # 添加保护等级字段
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
        bird_info = bird_info.query.get(bird_info_id)
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
    bird.geotype = geotype
    bird.seasonal = seasonal
    bird.IUCN = IUCN
    bird.level = level
    bird.describe = describe
    bird.habitat = habitat
    bird.behavior = behavior
    bird.bird_info = ','.join(map(str, bird_info_ids))
    bird.update()
    return Responser.response_success(msg="修改成功")

@inventory.route('/delete_bird', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])
def delete_bird(request):
    # 鸟类名录删除接口
    bird_id = request.json.get("bird_id")

    bird = BirdInventory.query.get(bird_id)
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')

    bird.is_lock = True
    bird.update()
    return Responser.response_success("删除成功")

@inventory.route('/get_all_birds', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin'])
def get_all_birds():
    # 鸟类名录查询所有接口
    query = BirdInventory.query

    # 添加模糊查询条件，根据目、科、种来匹配
    order_en = request.args.get("order_en")
    family_en = request.args.get("family_en")
    species = request.args.get("species")
    if order_en:
        query = query.filter(BirdInventory.order_en.ilike(f'%{order_en}%'))
    if family_en:
        query = query.filter(BirdInventory.family_en.ilike(f'%{family_en}%'))
    if species:
        query = query.filter(BirdInventory.species.ilike(f'%{species}%'))

    birds = query.all()
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
            'geotype': bird.geotype,
            'seasonal': bird.seasonal,
            'IUCN': bird.IUCN,
            'level': bird.level,
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
@login_required(['sysadmin', 'admin', 'others'])
def get_bird(request):
    # 鸟类名录查询单个接口
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
        'geotype': bird.geotype,
        'seasonal': bird.seasonal,
        'IUCN': bird.IUCN,
        'level': bird.level,
        'describe': bird.describe,
        'habitat': bird.habitat,
        'behavior': bird.behavior,
        'bird_info': bird.bird_info.split(',') if bird.bird_info else [],
        'create_at': bird.create_at,
        'update_at': bird.update_at,
    }
    return Responser.response_success(data=bird_dict)

@inventory.route('/create_bird_survey', methods=['POST'])
@requestPOST
@login_required(['sysadmin'])
def create_bird_survey(request):
    # 鸟类调查创建接口
    user_id = request.user_id
    survey_name = request.json.get("survey_name")
    survey_desc = request.json.get("survey_desc")
    survey_time = request.json.get("survey_time")
    survey_location = request.json.get("survey_location")
    describe = request.json.get("describe")
    habitat = request.json.get("habitat")
    behavior = request.json.get("behavior")
    bird_info_ids = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([survey_name, survey_time, survey_location, describe, habitat, behavior])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    invalid_bird_info_ids = []
    for bird_info_id in bird_info_ids:
        bird_info = bird_info.query.get(bird_info_id)
        if bird_info is None:
            invalid_bird_info_ids.append(bird_info_id)
    if invalid_bird_info_ids:
        return Responser.response_error('无效的鸟类声音图像信息ID: {}'.format(invalid_bird_info_ids))

    bird_survey = BirdSurvey(
        user_id=user_id,
        survey_name=survey_name,
        survey_desc=survey_desc,
        survey_time=survey_time,
        survey_location=survey_location,
        describe=describe,
        habitat=habitat,
        behavior=behavior,
        bird_info=','.join(map(str, bird_info_ids))
    )
    bird_survey.update()
    return Responser.response_success(msg="创建鸟类调查成功")
@inventory.route('/update_bird_survey', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def update_bird_survey(request):
    #鸟类调查更新接口
    bird_survey_id = request.json.get("bird_survey_id")
    user_id = request.user_id
    survey_name = request.json.get("survey_name")
    survey_desc = request.json.get("survey_desc")
    survey_time = request.json.get("survey_time")
    survey_location = request.json.get("survey_location")
    describe = request.json.get("describe")
    habitat = request.json.get("habitat")
    behavior = request.json.get("behavior")
    bird_info_ids = request.json.get("bird_info", [])

    bird_survey = BirdSurvey.query.get(bird_survey_id)
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')
    if bird_survey.user_id != user_id:
        return Responser.response_error('没有权限修改该鸟类调查')

    lost_attrs = required_attrs_validator([survey_name, survey_time, survey_location, describe, habitat, behavior])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    invalid_bird_info_ids = []
    for bird_info_id in bird_info_ids:
        bird_info = bird_info.query.get(bird_info_id)
        if bird_info is None:
            invalid_bird_info_ids.append(bird_info_id)
    if invalid_bird_info_ids:
        return Responser.response_error('无效的鸟类声音图像信息ID: {}'.format(invalid_bird_info_ids))

    bird_survey.survey_name = survey_name
    bird_survey.survey_desc = survey_desc
    bird_survey.survey_time = survey_time
    bird_survey.survey_location = survey_location
    bird_survey.describe = describe
    bird_survey.habitat = habitat
    bird_survey.behavior = behavior
    bird_survey.bird_info = ','.join(map(str, bird_info_ids))
    bird_survey.update()
    return Responser.response_success(msg="修改鸟类调查成功")

@inventory.route('/delete_bird_survey', methods=['GET'])
@requestGET
@login_required(['sysadmin','admin'])
def delete_bird_survey(request):
    # 鸟类调查删除接口
    bird_survey_id = request.json.get("bird_survey_id")

    bird_survey = BirdSurvey.query.get(bird_survey_id)
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')

    bird_survey.is_lock = True
    bird_survey.update()
    return Responser.response_success("删除鸟类调查成功")

@inventory.route('/get_all_bird_surveys', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin'])
def get_all_bird_surveys(request):
    #鸟类调查查询所有接口
    bird_surveys = BirdSurvey.query.filter_by().all()
    bird_survey_list = []
    for bird_survey in bird_surveys:
        bird_survey_dict = {
            'bird_survey_id': bird_survey.id,
            'user_id': bird_survey.user_id,
            'survey_name': bird_survey.survey_name,
            'survey_desc': bird_survey.survey_desc,
            'survey_time': bird_survey.survey_time,
            'survey_location': bird_survey.survey_location,
            'describe': bird_survey.describe,
            'habitat': bird_survey.habitat,
            'behavior': bird_survey.behavior,
            'bird_info': bird_survey.bird_info.split(',') if bird_survey.bird_info else [],
            'create_at': bird_survey.create_at,
            'update_at': bird_survey.update_at,
            'is_lock': bird_survey.is_lock
        }
        bird_survey_list.append(bird_survey_dict)
    return Responser.response_success(data=bird_survey_list)

@inventory.route('/get_bird_survey', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin', 'others'])
def get_bird_survey(request):
    #鸟类调查查询单个接口
    bird_survey_id = request.json.get("bird_survey_id")
    bird_survey = BirdSurvey.query.get(bird_survey_id)
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')
    bird_survey_dict = {
        'bird_survey_id': bird_survey.id,
        'user_id': bird_survey.user_id,
        'survey_name': bird_survey.survey_name,
        'survey_desc': bird_survey.survey_desc,
        'survey_time': bird_survey.survey_time,
        'survey_location': bird_survey.survey_location,
        'describe': bird_survey.describe,
        'habitat': bird_survey.habitat,
        'behavior': bird_survey.behavior,
        'bird_info': bird_survey.bird_info.split(',') if bird_survey.bird_info else [],
        'create_at': bird_survey.create_at,
        'update_at': bird_survey.update_at,
    }
    return Responser.response_success(data=bird_survey_dict)

# ...

@inventory.route('/create_bird_record', methods=['POST'])
@requestPOST
@login_required(['sysadmin'])
def create_bird_record(request):
    # 鸟类记录创建接口
    user_id = request.user_id
    bird_id = request.json.get("bird_id")
    record_time = request.json.get("record_time")
    record_location = request.json.get("record_location")
    longitude = request.json.get("longitude")
    latitude = request.json.get("latitude")
    weather = request.json.get("weather")
    temperature = request.json.get("temperature")
    record_describe = request.json.get("record_describe")
    bird_info_ids = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([bird_id, record_time, record_location, longitude, latitude, weather, temperature])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    invalid_bird_info_ids = []
    for bird_info_id in bird_info_ids:
        bird_info = bird_info.query.get(bird_info_id)
        if bird_info is None:
            invalid_bird_info_ids.append(bird_info_id)
    if invalid_bird_info_ids:
        return Responser.response_error('无效的鸟类声音图像信息ID: {}'.format(invalid_bird_info_ids))

    bird_record = BirdRecords(
        user_id=user_id,
        bird_id=bird_id,
        record_time=record_time,
        record_location=record_location,
        longitude=longitude,
        latitude=latitude,
        weather=weather,
        temperature=temperature,
        record_describe=record_describe,
        bird_info=','.join(map(str, bird_info_ids))
    )
    bird_record.update()
    return Responser.response_success(msg="创建鸟类记录成功")


@inventory.route('/update_bird_record', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def update_bird_record(request):
    # 鸟类记录更新接口
    bird_record_id = request.json.get("bird_record_id")
    user_id = request.user_id
    bird_id = request.json.get("bird_id")
    record_time = request.json.get("record_time")
    record_location = request.json.get("record_location")
    longitude = request.json.get("longitude")
    latitude = request.json.get("latitude")
    weather = request.json.get("weather")
    temperature = request.json.get("temperature")
    record_describe = request.json.get("record_describe")
    bird_info_ids = request.json.get("bird_info", [])

    bird_record = BirdRecords.query.get(bird_record_id)
    if bird_record is None:
        return Responser.response_error('找不到指定的鸟类记录')
    if bird_record.user_id != user_id:
        return Responser.response_error('没有权限修改该鸟类记录')

    lost_attrs = required_attrs_validator([bird_id, record_time, record_location, longitude, latitude, weather, temperature])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    invalid_bird_info_ids = []
    for bird_info_id in bird_info_ids:
        bird_info = bird_info.query.get(bird_info_id)
        if bird_info is None:
            invalid_bird_info_ids.append(bird_info_id)
    if invalid_bird_info_ids:
        return Responser.response_error('无效的鸟类声音图像信息ID: {}'.format(invalid_bird_info_ids))

    bird_record.bird_id = bird_id
    bird_record.record_time = record_time
    bird_record.record_location = record_location
    bird_record.longitude = longitude
    bird_record.latitude = latitude
    bird_record.weather = weather
    bird_record.temperature = temperature
    bird_record.record_describe = record_describe
    bird_record.bird_info = ','.join(map(str, bird_info_ids))
    bird_record.update()
    return Responser.response_success(msg="修改鸟类记录成功")


@inventory.route('/delete_bird_record', methods=['GET'])
@requestGET
@login_required(['sysadmin','admin'])
def delete_bird_record(request):
    # 鸟类记录删除接口
    bird_record_id = request.json.get("bird_record_id")

    bird_record = BirdRecords.query.get(bird_record_id)
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
    bird_records = BirdRecords.query.filter_by().all()
    bird_record_list = []
    for bird_record in bird_records:
        bird_record_dict = {
            'bird_record_id': bird_record.id,
            'user_id': bird_record.user_id,
            'bird_id': bird_record.bird_id,
            'record_time': bird_record.record_time,
            'record_location': bird_record.record_location,
            'longitude': bird_record.longitude,
            'latitude': bird_record.latitude,
            'weather': bird_record.weather,
            'temperature': bird_record.temperature,
            'record_describe': bird_record.record_describe,
            'bird_info': bird_record.bird_info.split(',') if bird_record.bird_info else [],
            'create_at': bird_record.create_at,
            'update_at': bird_record.update_at,
            'is_lock': bird_record.is_lock
        }
        bird_record_list.append(bird_record_dict)
    return Responser.response_success(data=bird_record_list)


@inventory.route('/get_bird_record', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin', 'others'])
def get_bird_record(request):
    # 鸟类记录获取单个接口
    bird_record_id = request.json.get("bird_record_id")
    bird_record = BirdRecords.query.get(bird_record_id)
    if bird_record is None:
        return Responser.response_error('找不到指定的鸟类记录')
    bird_record_dict = {
        'bird_record_id': bird_record.id,
        'user_id': bird_record.user_id,
        'bird_id': bird_record.bird_id,
        'record_time': bird_record.record_time,
        'record_location': bird_record.record_location,
        'longitude': bird_record.longitude,
        'latitude': bird_record.latitude,
        'weather': bird_record.weather,
        'temperature': bird_record.temperature,
        'record_describe': bird_record.record_describe,
        'bird_info': bird_record.bird_info.split(',') if bird_record.bird_info else [],
        'create_at': bird_record.create_at,
        'update_at': bird_record.update_at,
    }
    return Responser.response_success(data=bird_record_dict)

# ...
