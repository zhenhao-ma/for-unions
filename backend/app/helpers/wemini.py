from app.core.config import settings
import requests
from app import schemas
import base64
from Crypto.Cipher import AES
import json
from redis import Redis

access_token_key = f'wechat_app_access_token'


def js_code_to_session(js_code: str) -> schemas.Wechat.Code2SessionResponse:
    """wechat miniapp code in exchange for session_key + openid
    session_key should be private

    see:
    https://blog.51cto.com/u_15308668/3147509
    https://www.cnblogs.com/zzqit/p/9983407.html

    code: JS Code by frontend. wx.Login
    """
    openid_url = f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.WECHAT_APP_ID}&secret={settings.WECHAT_APP_SECRET}&js_code={js_code}&grant_type=authorization_code"
    req = requests.get(openid_url)
    rep = req.json()

    return schemas.Wechat.Code2SessionResponse(**rep)


def _get_new_access_token(appid, secret) -> schemas.Wechat.GetAccessTokenResponse:
    """https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/access-token/auth.getAccessToken.html"""
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
    req = requests.get(url)
    j = req.json()
    return schemas.Wechat.GetAccessTokenResponse(**j)


def get_access_token(redis: Redis, *, appid: str, secret: str) -> str:
    acc_token = redis.get(access_token_key)
    if acc_token is None:
        # get new access token
        res = _get_new_access_token(appid=appid, secret=secret)
        redis.set(access_token_key, res.access_token, int(res.expires_in - 60))
        acc_token = res.access_token
    return acc_token


def clear_access_token(redis: Redis):
    redis.delete(access_token_key)


def get_phone_number(redis: Redis, *, appid: str, secret: str, code: str, retried: bool = True) -> schemas.Wechat.GetPhoneNumberResponse:
    """https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/phonenumber/phonenumber.getPhoneNumber.html"""
    access_token = get_access_token(redis, appid=appid, secret=secret)
    url = f'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}'
    req = requests.post(url=url, json={
        'code': code
    })
    j = req.json()
    print("j: ", j)
    if "errcode" in j and j["errcode"] == 40001:
        if not retried:
            raise ValueError(f"Invalid access token")
        else:
            # access code invalid or not latest
            clear_access_token(redis)
            return get_phone_number(redis, appid=appid, secret=secret, code=code, retried=False)
    return schemas.Wechat.GetPhoneNumberResponse(**j)


class WXBizDataCrypt:
    """Decrypt Data, such as UserInfo of wechat App
    https://www.cnblogs.com/zzqit/p/9983407.html
    """

    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)

        encryptedData = base64.b64decode(encryptedData)

        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
