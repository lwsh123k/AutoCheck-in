from AESTool import AESTool
from WebVpnLogin import CheckInWithVpn
from dotenv import load_dotenv
import os

load_dotenv()
accounts = []


def handler(event, context):
    # 从.env读取账号 密码 pushKey
    env_vars = os.environ
    for key, value in env_vars.items():
        if key.startswith("ACCOUNT"):
            # 使用 & 分割字符串
            parts = value.split("&")
            if len(parts) == 3:
                username, password, push_token = parts
                print(username, password, push_token)
                accounts.append(
                    {
                        "username": username,
                        "password": password,
                        "push_token": push_token,
                    }
                )
    for account in accounts:
        print(account)
        # 账号. 密码. push-plus的token
        msg_push_token = account["push_token"]
        user_account = {"username": account["username"], "pwd": account["password"]}
        user_account["pwd"] = AESTool().aes_encrypt(user_account["pwd"])
        auto_check_in = CheckInWithVpn()

        # 签到: 登录webvpn, 获取签到结果, 消息推送
        auto_check_in.login_web_vpn(user_account)
        auto_check_in.sign_train()
        auto_check_in.message_push(msg_push_token)


handler(None, None)
