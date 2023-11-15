import requests
import time
from urllib.parse import urlparse, parse_qs
from AESTool import AESTool
from GetLocation import GetLocation


# this file is not used.
def get_token(user_account):
    session = requests.session()  # session会保存请求中的cookie
    host = "https://org.xjtu.edu.cn"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
            " Gecko) Chrome/116.0.0.0 Safari/537.36"
        ),
        "Referer": "https://pahw.xjtu.edu.cn/",
    }
    session.get(
        host
        + "/openplatform/oauth/authorize?"
        "appId=1529&redirectUri=https://pahw.xjtu.edu.cn/sso/callback&responseType=code&"
        "scope=user_info&state=1234",
        headers=headers,
    )

    # 登录
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
            " Gecko) Chrome/116.0.0.0 Safari/537.36"
        ),
        "Origin": "https://org.xjtu.edu.cn",
        "Referer": "https://org.xjtu.edu.cn/openplatform/login.html",
    }
    res = session.post(
        host + "/openplatform/g/admin/login",
        json={"loginType": 1, "jcaptchaCode": "", **user_account},
        headers=headers,
    )
    open_platform_user = res.json()["data"]["tokenKey"]
    member_id = res.json()["data"]["orgInfo"]["memberId"]
    # 注意这里的cookie, dict中的value也需要用双引号包裹
    requests.utils.add_dict_to_cookiejar(
        session.cookies,
        {
            "open_Platform_User": '"' + open_platform_user + '"',
            "memberId": '"' + str(member_id) + '"',
        },
    )

    # 获取用户信息(学号)
    timestamp_ms = int(time.time()) * 1000
    res = session.get(
        host + "/openplatform/g/admin/getUserIdentity",
        params={"memberId": member_id, "_": timestamp_ms},
    )
    person_no = res.json()["data"][0]["personNo"]

    # 获得认证的链接, 并提取auth code
    # https://pahw.xjtu.edu.cn/sso/callback?code=oauth_code_67cc04875300347e9935cf08f71ce1d9&state=1234&userType=1&employeeNo=312215
    # 提取code
    headers = {
        "Referer": "https://org.xjtu.edu.cn/openplatform/login.html",
    }
    res = session.get(
        host + "/openplatform/oauth/auth/getRedirectUrl",
        params={"userType": 1, "personNo": person_no, "_": int(time.time()) * 1000},
        headers=headers,
    )
    auth_url = res.json()["data"]
    parsed_auth_url = urlparse(auth_url)
    auth_code = parse_qs(parsed_auth_url.query)["code"][0]

    # 获得token
    headers = {
        "Referer": auth_url,
    }
    host = "https://ipahw.xjtu.edu.cn"
    res = session.get(
        host + "/szjy-boot/sso/codeLogin",
        params={"code": auth_code, "userType": 1, "employeeNo": person_no},
        headers=headers,
    )
    print(res.json())
    token = res.json()["data"]["token"]
    return token


def sign_train(token):
    url = "https://ipahw.xjtu.edu.cn/szjy-boot/api/v1/sportActa/signRun"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; MI 9 Build/QKQ1.190825.002; wv)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166"
            " Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0"
            " toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white"
            " fontIndex/0"
        ),
        "token": token,
        "content-type": "application/json",
        "Accept": "*/*",
        "Origin": "https://ipahw.xjtu.edu.cn",
        "X-Requested-With": "synjones.commerce.xjtu",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ipahw.xjtu.edu.cn/pages/index/hdgl/hdgl_run?courseType=7&signType=1&activityAddress=&courseInfoId=1698877075970076673",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    # 获取当前经纬度信息
    latitude, longitude = GetLocation().get_current_location()
    res = requests.post(
        url,
        headers=headers,
        json={
            "sportType": 2,
            "longitude": 108.652927,
            "latitude": 34.256757,
            "courseInfoId": "1698877075970076673",
        },
    )
    print(res.json())


def sign_out_train(token):
    url = "https://ipahw.xjtu.edu.cn/szjy-boot/api/v1/sportActa/signOutTrain"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; MI 9 Build/QKQ1.190825.002; wv)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166"
            " Mobile Safari/537.36 toon/2122313098 toonType/150 toonVersion/6.3.0"
            " toongine/1.0.12 toongineBuild/12 platform/android language/zh skin/white"
            " fontIndex/0"
        ),
        "token": token,
        "content-type": "application/json",
        "Accept": "*/*",
        "Origin": "https://ipahw.xjtu.edu.cn",
        "X-Requested-With": "synjones.commerce.xjtu",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ipahw.xjtu.edu.cn/pages/index/hdgl/hdgl_run?courseType=7&signType=2&activityAddress=&courseInfoId=1698877075970076673",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    res = requests.post(url, headers=headers, json={})
    print(res.json())


if __name__ == "__main__":
    # 输入明文账号密码，密码使用aes加密
    user_account = {"username": "xxx", "pwd": "xxx"}
    user_account["pwd"] = AESTool().aes_encrypt(user_account["pwd"])
    print(user_account)
    # 签到
    token = get_token(user_account)
    sign_train(token)
    # 等待1h
    # time.sleep(60 * 60)
    # 签退
    token = get_token(user_account)
    sign_out_train(token)
