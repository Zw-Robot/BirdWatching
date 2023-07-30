#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------
@Author:Robot
@Time:2023-07-15:10:59
--------------------------------------------
"""
import uuid
from datetime import datetime
from math import ceil

from apps.components.common import required_attrs_validator
from apps.inventory import inventory
from apps.models import BirdInventory, BirdSurvey, BirdRecords, BirdInfos
from apps.components.middleware import requestPOST, login_required, requestGET
from apps.components.responser import Responser, FileResponser


@inventory.route('/create_bird', methods=['POST'])
@requestPOST
# @login_required(['sysadmin'])
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

    infos_id = []
    for info in bird_infos:
        for sound in info.get("sound", []):
            path = FileResponser.audio_save(sound, "inventory", "inventory_sound_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=username, path=path, label="sound")
            temp.update()
            infos_id.append(temp.id)
        for image in info.get("image", []):
            path = FileResponser.image_save(image, "inventory", "inventory_image_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=username, path=path, label="image")
            temp.update()
            infos_id.append(temp.id)
        for video in info.get("video", []):
            path = FileResponser.video_save(video, "inventory", "inventory_video_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=username, path=path, label="video")
            temp.update()
            infos_id.append(temp.id)

    bird = BirdInventory(
        order_en=order_en,
        order_cn=order_cn,
        family_en=family_en,
        family_cn=family_cn,
        genus=genus,
        species=species,
        latin_name=latin_name,
        geotype = geotype,
        seasonal = seasonal,
        IUCN = IUCN,
        level = level,
        describe=describe,
        habitat=habitat,
        behavior=behavior,
        bird_info=','.join(map(str, infos_id))
    )
    bird.update()
    return Responser.response_success(msg="创建成功")


@inventory.route('/update_bird', methods=['POST'])
@requestPOST
# @login_required(['sysadmin', 'admin','others'])
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
    geotype = request.json.get("geotype","")
    seasonal = request.json.get("seasonal","")
    IUCN = request.json.get("IUCN","")
    level = request.json.get("level","")
    describe = request.json.get("describe", "")
    habitat = request.json.get("habitat", "")
    behavior = request.json.get("behavior", "")
    bird_infos = request.json.get("bird_info", [])  # {"sound":[],"image":[],"video":[]}

    lost_attrs = required_attrs_validator([bird_id, username])
    if lost_attrs:
        return Responser.response_error('缺少参数')
    bird = BirdInventory.query.get(bird_id)
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')

    infos_id = []
    for info in bird_infos:
        for sound in info.get("sound", []):
            path = FileResponser.audio_save(sound, "inventory", "inventory_sound_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=username, path=path, label="sound")
            temp.update()
            infos_id.append(temp.id)
        for image in info.get("image", []):
            path = FileResponser.image_save(image, "inventory", "inventory_image_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=username, path=path, label="image")
            temp.update()
            infos_id.append(temp.id)
        for video in info.get("video", []):
            path = FileResponser.video_save(video, "inventory", "inventory_video_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=username, path=path, label="video")
            temp.update()
            infos_id.append(temp.id)

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
    bird.bird_info = ','.join(map(str, infos_id)) if infos_id else bird.bird_info

    bird.update()
    return Responser.response_success(msg="修改成功")


@inventory.route('/delete_bird', methods=['GET'])
@requestGET
# @login_required(['sysadmin', 'admin'])
def delete_bird(request):
    # 鸟类记录删除接口
    bird_id = request.json.get("bird_id")

    bird = BirdInventory.query.get(bird_id)
    if bird is None:
        return Responser.response_error('找不到指定的鸟类信息')

    bird.is_lock = True
    bird.update()
    return Responser.response_success("删除成功")


@inventory.route('/get_all_birds', methods=["GET"])
@requestGET
# @login_required(['sysadmin', 'admin'])
def get_all_birds(request):
    # 鸟类名录查询所有接口
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    bird_inventory_query = BirdInventory.query.filter_by(is_lock=False)

    total_pages = ceil(bird_inventory_query.count() / per_page)

    birds = bird_inventory_query.paginate(page=page, per_page=per_page)

    bird_list = []
    for bird in birds:
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
            "geotype" : bird.geotype,
            "seasonal" : bird.seasonal,
            "IUCN" : bird.IUCN,
            "level" : bird.level,
            'describe': bird.describe,
            'habitat': bird.habitat,
            'behavior': bird.behavior,
            'bird_info': files,
            'create_at': bird.create_at,
            'update_at': bird.update_at,
            'is_lock': bird.is_lock
        }
        bird_list.append(bird_dict)
    return Responser.response_page(data=bird_list,count=total_pages,page=page,page_size=per_page)


@inventory.route('/get_bird', methods=["GET"])
@requestGET
# @login_required(['sysadmin', 'admin','others'])
def get_bird(request):
    # 鸟类名录查询单个接口
    bird_id = request.json.get("bird_id")
    bird = BirdInventory.query.get(bird_id)
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
        "geotype" : bird.geotype,
        "seasonal" : bird.seasonal,
        "IUCN" : bird.IUCN,
        "level" : bird.level,
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
    bird_infos = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([survey_name, survey_time, survey_location, describe, habitat, behavior])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    infos_id = []
    for info in bird_infos:
        for sound in info.get("sound", []):
            path = FileResponser.audio_save(sound, "inventory", "inventory_sound_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="sound")
            temp.update()
            infos_id.append(temp.id)
        for image in info.get("image", []):
            path = FileResponser.image_save(image, "inventory", "inventory_image_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="image")
            temp.update()
            infos_id.append(temp.id)
        for video in info.get("video", []):
            path = FileResponser.video_save(video, "inventory", "inventory_video_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="video")
            temp.update()
            infos_id.append(temp.id)
    bird_survey = BirdSurvey(
        user_id=user_id,
        survey_name=survey_name,
        survey_desc=survey_desc,
        survey_time=survey_time,
        survey_location=survey_location,
        describe=describe,
        habitat=habitat,
        behavior=behavior,
        bird_info=bird_infos
    )
    bird_survey.update()
    return Responser.response_success(msg="创建鸟类调查成功")


@inventory.route('/update_bird_survey', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def update_bird_survey(request):
    # 鸟类调查更新接口
    bird_survey_id = request.json.get("bird_survey_id")
    user_id = request.user_id
    survey_name = request.json.get("survey_name", "")
    survey_desc = request.json.get("survey_desc", "")
    survey_time = request.json.get("survey_time", "")
    survey_location = request.json.get("survey_location", "")
    describe = request.json.get("describe", "")
    habitat = request.json.get("habitat", "")
    behavior = request.json.get("behavior", "")
    bird_infos = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([bird_survey_id, user_id])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    bird_survey = BirdSurvey.query.get(bird_survey_id)
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')
    if bird_survey.user_id != user_id:
        return Responser.response_error('没有权限修改该鸟类调查')

    infos_id = []
    for info in bird_infos:
        for sound in info.get("sound", []):
            path = FileResponser.audio_save(sound, "inventory", "inventory_sound_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="sound")
            temp.update()
            infos_id.append(temp.id)
        for image in info.get("image", []):
            path = FileResponser.image_save(image, "inventory", "inventory_image_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="image")
            temp.update()
            infos_id.append(temp.id)
        for video in info.get("video", []):
            path = FileResponser.video_save(video, "inventory", "inventory_video_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="video")
            temp.update()
            infos_id.append(temp.id)

    bird_survey.survey_name = survey_name if survey_name else bird_survey.survey_name
    bird_survey.survey_desc = survey_desc if survey_desc else bird_survey.survey_desc
    bird_survey.survey_time = survey_time if survey_time else bird_survey.survey_time
    bird_survey.survey_location = survey_location if survey_location else bird_survey.survey_location
    bird_survey.describe = describe if describe else bird_survey.describe
    bird_survey.habitat = habitat if habitat else bird_survey.habitat
    bird_survey.behavior = behavior if behavior else bird_survey.behavior
    bird_survey.bird_info = ','.join(map(str, infos_id)) if infos_id else bird_survey.bird_info
    bird_survey.update()
    return Responser.response_success(msg="修改鸟类调查成功")


@inventory.route('/delete_bird_survey', methods=['GET'])
@requestGET
# @login_required(['sysadmin', 'admin'])
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
# @login_required(['sysadmin', 'admin'])
def get_all_bird_surveys(request):
    # 鸟类调查查询所有接口
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    bird_surveys_query = BirdSurvey.query.filter_by(is_lock=False)

    total_pages = ceil(bird_surveys_query.count() / per_page)

    bird_surveys = bird_surveys_query.paginate(page=page, per_page=per_page)

    bird_survey_list = []

    def process_bird_survey(bird_survey):
        files = []
        infos = bird_survey.bird_info.split(',') if bird_survey.bird_info else []
        for info in infos:
            temp = BirdInfos.query.get(info)
            files.append(FileResponser.get_path(temp.path if temp else "", temp.label if temp else ""))
        return {
            'bird_survey_id': bird_survey.id,
            'user_id': bird_survey.user_id,
            'survey_name': bird_survey.survey_name,
            'survey_desc': bird_survey.survey_desc,
            'survey_time': bird_survey.survey_time,
            'survey_location': bird_survey.survey_location,
            'describe': bird_survey.describe,
            'habitat': bird_survey.habitat,
            'behavior': bird_survey.behavior,
            'bird_info': files,
            'create_at': bird_survey.create_at,
            'update_at': bird_survey.update_at,
            'is_lock': bird_survey.is_lock
        }

    bird_survey_list = [process_bird_survey(bird_survey) for bird_survey in bird_surveys]
    return Responser.response_page(data=bird_survey_list,count=total_pages,page=page,page_size=per_page)


@inventory.route('/get_bird_survey', methods=["GET"])
@requestGET
# @login_required(['sysadmin', 'admin', 'others'])
def get_bird_survey(request):
    # 鸟类调查查询单个接口
    bird_survey_id = request.json.get("bird_survey_id")
    bird_survey = BirdSurvey.query.get(bird_survey_id)
    if bird_survey is None:
        return Responser.response_error('找不到指定的鸟类调查信息')
    files = []
    infos = bird_survey.bird_info.split(',') if bird_survey.bird_info else []
    for info in infos:
        temp = BirdInfos.query.get(info)
        files.append(FileResponser.get_path(temp.path if temp.path else "", temp.label))
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
        'bird_info': files,
        'create_at': bird_survey.create_at,
        'update_at': bird_survey.update_at,
    }
    return Responser.response_success(data=bird_survey_dict)


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
    bird_infos = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([bird_id, record_time, record_location])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    infos_id = []
    for info in bird_infos:
        for sound in info.get("sound", []):
            path = FileResponser.audio_save(sound, "inventory", "inventory_sound_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="sound")
            temp.update()
            infos_id.append(temp.id)
        for image in info.get("image", []):
            path = FileResponser.image_save(image, "inventory", "inventory_image_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="image")
            temp.update()
            infos_id.append(temp.id)
        for video in info.get("video", []):
            path = FileResponser.video_save(video, "inventory", "inventory_video_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="video")
            temp.update()
            infos_id.append(temp.id)

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
        bird_info=','.join(map(str, infos_id))
    )
    bird_record.update()
    return Responser.response_success(msg="创建鸟类记录成功")


@inventory.route('/update_bird_record', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def update_bird_record(request):
    # 鸟类记录更新接口
    bird_record_id = request.json.get("bird_record_id")
    user_id = request.json.get("user_id")
    bird_id = request.json.get("bird_id")
    record_time = request.json.get("record_time", "")
    longitude = request.json.get("longitude", "")
    latitude = request.json.get("latitude", "")
    weather = request.json.get("weather", "")
    temperature = request.json.get("temperature", "")
    record_location = request.json.get("record_location", "")
    record_describe = request.json.get("record_describe", "")
    bird_infos = request.json.get("bird_info", [])

    lost_attrs = required_attrs_validator([user_id, bird_id, bird_record_id])
    if lost_attrs:
        return Responser.response_error('缺少参数')

    bird_record = BirdRecords.query.get(bird_record_id)
    if bird_record is None:
        return Responser.response_error('找不到指定的鸟类记录')
    if bird_record.user_id != user_id:
        return Responser.response_error('没有权限修改该鸟类记录')

    infos_id = []
    for info in bird_infos:
        for sound in info.get("sound", []):
            path = FileResponser.audio_save(sound, "inventory", "inventory_sound_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="sound")
            temp.update()
            infos_id.append(temp.id)
        for image in info.get("image", []):
            path = FileResponser.image_save(image, "inventory", "inventory_image_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="image")
            temp.update()
            infos_id.append(temp.id)
        for video in info.get("video", []):
            path = FileResponser.video_save(video, "inventory", "inventory_video_{}".format(str(uuid.uuid1())))
            temp = BirdInfos(order_by=user_id, path=path, label="video")
            temp.update()
            infos_id.append(temp.id)

    bird_record.bird_id = bird_id if bird_id else bird_record.bird_id
    bird_record.record_time = record_time if record_time else bird_record.record_time
    bird_record.record_location = record_location if record_location else bird_record.record_location
    bird_record.record_describe = record_describe if record_describe else bird_record.record_describe
    bird_record.longitude = longitude if longitude else bird_record.longitude
    bird_record.latitude = latitude if latitude else bird_record.latitude
    bird_record.weather = weather if weather else bird_record.weather
    bird_record.temperature = temperature if temperature else bird_record.temperature
    bird_record.bird_info = ','.join(map(str, infos_id)) if infos_id else bird_record.bird_info
    bird_record.update()
    return Responser.response_success(msg="修改鸟类记录成功")


@inventory.route('/delete_bird_record', methods=['GET'])
@requestGET
# @login_required(['sysadmin', 'admin'])
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
# @login_required(['sysadmin', 'admin'])
def get_all_bird_records(request):
    # 鸟类记录获取所有接口

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    bird_records_query = BirdRecords.query.filter_by(is_lock=False)

    total_pages = ceil(bird_records_query.count() / per_page)

    bird_records = bird_records_query.paginate(page=page, per_page=per_page)

    bird_record_list = []
    for bird_record in bird_records:
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
            'bird_info': files,
            'create_at': bird_record.create_at,
            'update_at': bird_record.update_at,
            'is_lock': bird_record.is_lock
        }
        bird_record_list.append(bird_record_dict)
    return Responser.response_page(data=bird_record_list,count=total_pages,page=page,page_size=per_page)


@inventory.route('/get_bird_record', methods=["GET"])
@requestGET
def get_bird_record(request):
    # 鸟类记录获取单个接口
    bird_record_id = request.json.get("bird_record_id")
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
