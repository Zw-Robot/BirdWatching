from flask import jsonify, make_response

from . import status
class Responser:
    @staticmethod
    def response_success(data=None, msg='success', count=None, **kwargs):
        """
        请求成功返回
        :param data: 返回的数据
        :param msg: 返回提示信息
        :param count: 数量信息
        :return:
        """
        wrapper = {
            'code': 0,
            'msg': msg, **kwargs
        }
        if data is not None:
            wrapper['data'] = data
        if count is not None:
            wrapper['count'] = count
        return jsonify(wrapper, status.HTTP_200_OK)

    @staticmethod
    def response_error(msg='server error', code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        """
        返回系统错误
        :param msg: 错误信息
        :param code: 错误码
        :return:
        """
        wrapper = {
            'code': code,
            'msg': msg
        }
        return jsonify(wrapper, status.HTTP_200_OK)

    @staticmethod
    def response_page(data, count, page, page_size, msg='success', **kwargs):
        """
        返回分页数据
        :param data: 返回的数据
        :param msg: 返回提示信息
        :param count: 数量信息
        :param page: 第几页
        :param page_size: 每页数量
        :Param kwargs: 附加字段
        :return:
        """
        wrapper = {
            'code': 0,
            'msg': msg,
            'count': count,
            'page': page,
            'page_size': page_size,
            'data': data
        }
        for k, v in kwargs.items():
            wrapper[k] = v
        return jsonify(wrapper, status.HTTP_200_OK)

    @staticmethod
    def response_page_with_total(data, total, count, page, page_size, msg='success', **kwargs):
        """
        返回分页数据
        :param data: 返回的数据
        :param total: 返回的聚合数据
        :param msg: 返回提示信息
        :param count: 数量信息
        :param page: 第几页
        :param page_size: 每页数量
        :Param kwargs: 附加字段
        :return:
        """
        wrapper = {
            'code': 0,
            'msg': msg,
            'count': count,
            'page': page,
            'total': total,
            'page_size': page_size,
            'data': data
        }
        for k, v in kwargs.items():
            wrapper[k] = v
        return jsonify(wrapper, status.HTTP_200_OK)

class FileResponser:

    @staticmethod
    def response_success(file_io):
        import os
        file_name = os.path.relpath(file_io.name)
        if file_name.startswith('_'):
            file_name = file_name[1:]
        response = make_response(file_io)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Access-Control-Expose-Headers'] = 'Content-disposition'
        response.headers['Content-Disposition'] = 'attachment;filename="%s"' % (file_name)
        return response

    @staticmethod
    def image_save(image=None, path=None, filename=None):
        if not path and not image:
            savepath = '/robot/birdwatching/var/images/default.png'
        else:
            savepath = '/robot/birdwatching/var/images/{}/{}'.format(path, filename)

        if image:
            image.save(savepath)
        return savepath

    @staticmethod
    def get_image(path,filename):
        if not path:
            savepath = '/robot/birdwatching/var/images/default.png'
        else:
            savepath = '/robot/birdwatching/var/images/{}/{}'.format(path, filename)
        image_data ={
            "file_name":filename,
            "url":savepath
        }
        return image_data