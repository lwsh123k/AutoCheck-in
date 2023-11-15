import requests
import time
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from AESTool import AESTool


class CheckInWithVpn:
    def __int__(self):
        self.session = None
        self.token = None
        self.result_data = None

    def login_web_vpn(self, user_account):
        host = "https://webvpn.xjtu.edu.cn"
        session = requests.session()
        # 登录到web vpn. 服务器会通过set cookie的方式给本地浏览器一个唯一标识
        session.get(host + "/login?oauth_login=true HTTP/1.1")

        # 账号密码登录
        res = session.post(
            host
            + "/https/77726476706e69737468656265737421ffe546d23f3a7c45300d8db9d6562d/openplatform/g/admin/login?vpn-12-o2-org.xjtu.edu.cn",
            json={"loginType": 1, "jcaptchaCode": "", **user_account},
        )
        tokenKey = res.json()["data"]["tokenKey"]
        memberId = str(res.json()["data"]["orgInfo"]["memberId"])  # 个人在学校的id
        print(memberId)
        session.post(
            host
            + "/wengine-vpn/cookie?method=set&host=org.xjtu.edu.cn&scheme=https&path=/openplatform/login.html&ck_data=open_Platform_User="
            + tokenKey
            + "; path=/;"
        )
        session.post(
            host
            + "/wengine-vpn/cookie?method=set&host=org.xjtu.edu.cn&scheme=https&path=/openplatform/login.html&ck_data=memberId="
            + memberId
            + "; path=/;"
        )

        # 获取个人身份信息
        res = session.get(
            host
            + "/https/77726476706e69737468656265737421ffe546d23f3a7c45300d8db9d6562d/openplatform/g/admin/getUserIdentity?vpn-12-o2-org.xjtu.edu.cn&memberId="
            + memberId
            + "&_="
            + str(int(time.time()) * 1000)
        )
        print(res.json())
        person_no = res.json()["data"][0]["personNo"]
        res = session.get(
            host
            + "/https/77726476706e69737468656265737421ffe546d23f3a7c45300d8db9d6562d/openplatform/oauth/auth/getRedirectUrl?vpn-12-o2-org.xjtu.edu.cn&userType=1&personNo="
            + person_no
            + "&_="
            + str(int(time.time()) * 1000)
        )
        print(res.json())
        auth_url = res.json()["data"]
        parsed_auth_url = urlparse(auth_url)
        auth_code = parse_qs(parsed_auth_url.query)["code"][0]
        print(auth_url)
        session.get(
            host
            + "/http/77726476706e69737468656265737421e7f2438a373e2648741c9ce29d51367b9724/login?oauth_login=true&code="
            + auth_code
            + "&state=1234&userType=1&employeeNo="
            + person_no
        )
        # 登录到体美劳平台
        res = session.get(
            host
            + "/https/77726476706e69737468656265737421ffe546d23f3a7c45300d8db9d6562d/openplatform/oauth/authorize?appId=1529&redirectUri"
            + "=https://pahw.xjtu.edu.cn/sso/callback&responseType=code&scope=user_info&state=1234"
        )
        parsed_auth_url = urlparse(res.url)
        auth_code = parse_qs(parsed_auth_url.query)["code"][0]
        print(res.url)
        res = session.get(
            host
            + "/https/77726476706e69737468656265737421e0f6498b692862446b468ca88d1b203b/szjy-boot/sso/codeLogin?vpn-12-o2-pahw.xjtu.edu.cn&code="
            + auth_code
            + "&userType=1&employeeNo="
            + person_no
        )
        token = res.json()["data"]["token"]
        print(token)
        # 将token和其他header参数设置到session中
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 10; MI 9 Build/QKQ1.190825.002; wv)"
                " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0"
                " Chrome/115.0.5790.166 Mobile Safari/537.36 toon/2122313098"
                " toonType/150 toonVersion/6.3.0 toongine/1.0.12 toongineBuild/12"
                " platform/android language/zh skin/white fontIndex/0"
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
        session.headers.update(headers)
        self.session = session

    def sign_train(self):
        session = self.session
        host = "https://webvpn.xjtu.edu.cn"
        url = "https://ipahw.xjtu.edu.cn/szjy-boot/api/v1/sportActa/signRun"
        res = session.post(
            host
            + "/https/77726476706e69737468656265737421e0f6498b692862446b468ca88d1b203b/szjy-boot/api/v1/sportActa/signRun?vpn-12-o2-pahw.xjtu.edu.cn",
            json={
                "sportType": 2,
                "longitude": 108.652927,
                "latitude": 34.256757,
                "courseInfoId": "1698877075970076673",
            },
        )
        self.result_data = res.json()
        current_time = datetime.today().strftime("%Y-%m-%d")
        self.result_data["sign-in-time"] = current_time
        print(res.json())

    def sign_out_train(self):
        session = self.session
        host = "https://webvpn.xjtu.edu.cn"
        url = "https://ipahw.xjtu.edu.cn/szjy-boot/api/v1/sportActa/signOutTrain"
        res = session.post(
            host
            + "/https/77726476706e69737468656265737421e0f6498b692862446b468ca88d1b203b/szjy-boot/api/v1/sportActa/signOutTrain?vpn-12-o2-pahw.xjtu.edu.cn",
            json={},
        )
        self.result_data = res.json()
        current_time = datetime.today().strftime("%Y-%m-%d")
        self.result_data["sign-out-time"] = current_time
        print(res.json())

    def message_push(self, token):
        json_data = {
            "token": token,
            "title": "标题",
            "content": self.result_data,
            "template": "json",
        }
        requests.post("http://www.pushplus.plus/send", json=json_data)
