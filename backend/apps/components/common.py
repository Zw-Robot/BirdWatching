from flask import jsonify


def required_attrs_validator(attrs):
    """
    必填参数校验， 后期将替换为 pydantic 或其他更规范的校验方式
    Args:
        attrs:

    Returns:

    """
    lost_attrs = []
    for foo in attrs:
        if foo is None:
            # todo: is None or not?
            lost_attrs.append(foo)

    return lost_attrs
