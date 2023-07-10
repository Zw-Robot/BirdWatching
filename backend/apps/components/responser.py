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

class FileResponder:
    """目前对文件下载了解不是很深入, 暂没有做过多的设计, 当前支持Excel格式文件的下载"""

    @classmethod
    def response_success(cls, file_io):
        from urllib.parse import quote
        import os
        file_name = os.path.relpath(file_io.name)
        # file_name = quote(file_name)
        if file_name.startswith('_'):
            file_name = file_name[1:]
        response = FileResponse(file_io)
        response['Content-Type'] = 'tapplication/vnd.ms-excel'
        response["Access-Control-Expose-Headers"] = "Content-disposition"
        response['Content-Disposition'] = 'attachment;filename="%s"' % (file_name)
        return response
