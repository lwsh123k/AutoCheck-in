from AESTool import AESTool
from WebVpnLogin import CheckInWithVpn


def handler(event, context):
    # 账号. 密码. push-plus的token
    msg_push_token = "xxx"
    user_account = {"username": "xxx", "pwd": "xxx"}
    user_account["pwd"] = AESTool().aes_encrypt(user_account["pwd"])
    auto_check_in = CheckInWithVpn()

    # 签到: 登录webvpn, 获取签到结果, 消息推送
    auto_check_in.login_web_vpn(user_account)
    auto_check_in.sign_train()
    auto_check_in.message_push(msg_push_token)

