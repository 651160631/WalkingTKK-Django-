import jpush
from jpush import common

app_key = "000028cebe5afa0500000000"
master_secret = "0000eb90c20366f400000000"

_jpush = jpush.JPush(app_key, master_secret)
# _jpush.set_logging("DEBUG")


def push_all(msg):
    push = _jpush.create_push()
    push.audience = jpush.all_
    push.notification = jpush.notification(alert=msg)
    push.platform = jpush.all_
    try:
        response=push.send()
        return None
    except common.Unauthorized:
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn")
    except common.JPushFailure:
        return "推送失败"
    except Exception as e:
        return "推送失败 - 原因: " + str(e)


def push_one(reg_id, msg):
    try:
        push = _jpush.create_push()
        push.audience = jpush.audience(
                jpush.registration_id(reg_id),
                )
        push.notification = jpush.notification(alert=msg)
        push.platform = jpush.all_
        push.send()
        return None
    except Exception as e:
        return "推送失败 - 原因: " + str(e)


def notification_all(msg, type):
    try:
        push = _jpush.create_push()

        push.audience = jpush.all_
        push.platform = jpush.all_

        ios = jpush.ios(alert=msg, sound="a.caf", extras={'msg_type': type}, badge='+1')
        android = jpush.android(alert=msg, priority=1, style=1, alert_type=1,
                                extras={'msg_type': type})
        push.notification = jpush.notification( android=android, ios=ios)
        result = push.send()
    except Exception as e:
        return "推送失败 - 原因: " + str(e)


def notification_one(reg_id, msg, type):
    try:
        push = _jpush.create_push()
        push.audience = jpush.audience(
                    jpush.registration_id(reg_id),
                    )
        push.platform = jpush.all_
        ios = jpush.ios(alert=msg, sound="a.caf", extras={'msg_type': type}, badge='+1')
        android = jpush.android(alert=msg, priority=1, style=1, alert_type=1,
                                extras={'msg_type': type})
        push.notification = jpush.notification( android=android, ios=ios)
        result = push.send()
        return None
    except Exception as e:
        return "推送失败 - 原因: " + str(e)


# notification_one(reg_id="191e35f7e07c73318fa", msg="测试notification333",type="jw")

# push_one("191e35f7e07c73318fa", "测试，收到请和我联系！22222222")
