from apps.components.middleware import requestGET, SingAuth, requestPOST, login_required
from apps.components.responser import Responser
from apps.models import SystemNotifications, Feedbacks
from apps.notice import notice



@notice.route('/get_feedbacks', methods=['GET'])
@requestGET
@login_required(['sysadmin', 'admin', 'others'])
def get_feedbacks(request):
    feedbacks = Feedbacks.query.all()

    feedback_list = []
    for feedback in feedbacks:
        feedback_data = {
            "id": feedback.id,
            "user_id": feedback.user_id,
            "feedback_text": feedback.feedback_text,
            "resolve_res": feedback.resolve_res,
            "create_at": feedback.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_resolved": feedback.is_resolved
        }
        feedback_list.append(feedback_data)

    return Responser.response_success(data=feedback_list)


@notice.route('/wx_get_feedbacks', methods=['GET'])
@requestGET
@SingAuth
def wx_get_feedbacks(request):
    user_id = int(request.args.get("user_id"))
    feedbacks = Feedbacks.query.filter_by(user_id=user_id)

    feedback_list = []
    for feedback in feedbacks:
        feedback_data = {
            "id": feedback.id,
            "user_id": feedback.user_id,
            "feedback_text": feedback.feedback_text,
            "resolve_res":feedback.resolve_res,
            "create_at": feedback.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_resolved": feedback.is_resolved
        }
        feedback_list.append(feedback_data)

    return Responser.response_success(data=feedback_list)


@notice.route('/create_feedbacks', methods=['POST'])
@requestPOST
@SingAuth
def create_feedbacks(request):
    user_id = int(request.json.get("user_id"))
    feedback_text = request.json.get("feedback_text")
    Feedbacks(user_id=user_id,feedback_text=feedback_text).update()
    return Responser.response_success(msg="创建成功")


@notice.route('/resolve_feedbacks', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def resolve_feedbacks(request):
    id = int(request.json.get("id",'-1'))
    resolve_res = request.json.get("resolve",'')
    fe = Feedbacks.query.filter_by(id=id).first()
    if fe:
        fe.is_resolved = True
        fe.resolve_res = resolve_res
        fe.update()
    else:
        return Responser.response_error(msg='没有该反馈')
    return Responser.response_success(msg="处理成功")

@notice.route('/create_system_notification', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def create_system_notification(request):
    title = request.json.get("title")
    content = request.json.get("content")

    if not title or not content:
        return Responser.response_error('缺少参数')

    notification = SystemNotifications(title=title, content=content)
    notification.update()

    return Responser.response_success(msg="系统通知创建成功")


@notice.route('/get_system_notifications', methods=['GET'])
@requestGET
def get_system_notifications(request):
    notifications = SystemNotifications.query.filter_by(is_lock=False)

    notification_list = []
    for notification in notifications:
        notification_data = {
            "id": notification.id,
            "title": notification.title,
            "content": notification.content,
            "create_at": notification.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_lock": notification.is_lock
        }
        notification_list.append(notification_data)

    return Responser.response_success(data=notification_list)


@notice.route('/delete_system_notice', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin'])  # 添加登录验证装饰器
def delete_system_notice(request):
    id = int(request.json.get("id", -1))
    notifications = SystemNotifications.query.filter_by(id=id)
    if notifications:
        notifications.is_lock = True
    else:
        return Responser.response_error('不存在该通知')

    return Responser.response_success(msg='删除成功')
