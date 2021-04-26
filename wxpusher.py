# -*- encoding: utf-8 -*-
import requests
import time


class template_push:
    base_url = "https://api.weixin.qq.com/cgi-bin"
    token = ""
    timestamp = 0

    def __init__(self, appID, appsecret, template_id):
        """
        初始化
        :param appID:
        :param appsecret:
        :param template_id:模板ID
        """
        self.appID = appID
        self.appsecret = appsecret
        self.template_id = template_id

    def get_token(self, force=False):
        """
        获取access_token，若过期则更新
        refer：https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html
        :return: None
        """
        if int(time.time()) >= self.timestamp or force:
            r = requests.get(
                f"{self.base_url}/token?grant_type=client_credential&appid={self.appID}&secret={self.appsecret}")
            result = r.json()
            if result.get("access_token"):
                self.token = result["access_token"]
                self.timestamp = int(time.time() + result["expires_in"])
            else:
                if result["errcode"] == -1:
                    time.sleep(3)
                    self.get_token()
                else:
                    raise Exception(f"get_token error!{result['errmsg']}")

    def push(self, touser, content):
        """
        发送模板消息
        refer：https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#5
        :param touser: 接收者的openid
        :param content: 消息内容
        :return: 布尔值 是否成功
        """
        self.get_token()
        json_data = {'touser': touser,
                     'template_id': self.template_id,
                     'data': {"content": {"value": content}}}
        r = requests.post(
            f"{self.base_url}/message/template/send?access_token={self.token}",
            json=json_data)
        errCode = r.json()["errcode"]
        if errCode != 0:
            print(r.json()["errmsg"])
            return False
        elif errCode == 40014 or errCode == 42001 or errCode == 42007:
            self.get_token(force=True)
        else:
            return True


class qyweixin:
    base_url = "https://qyapi.weixin.qq.com/cgi-bin"

    def __init__(self, corpid, secret, agentid):
        self.corpid = corpid
        self.secret = secret
        self.agentid = int(agentid)
        self.token = self.get_token()

    def get_token(self):
        """
        获取access_token
        有效期7200s（2小时）
        refer:https://work.weixin.qq.com/api/doc/10013#%E7%AC%AC%E4%B8%89%E6%AD%A5%EF%BC%9A%E8%8E%B7%E5%8F%96access_token
        :return:access_token
        """
        url = self.base_url + \
            f"/gettoken?corpid={self.corpid}&corpsecret={self.secret}"
        r = requests.get(url)
        result = r.json()
        if result["errcode"] == 0:
            self.token = result["access_token"]
            return self.token
        else:
            raise Exception(f"get_token error!{result['errmsg']}")

    def push(self, content: str, touser="", toparty="", totag=""):
        """
        推送消息
        refer：https://work.weixin.qq.com/api/doc/90001/90143/90372
        :param content:消息内容，最长不超过2048个字节，超过将截断
        :param touser:指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔）特殊情况：指定为”@all”，则向该企业应用的全部成员发送
        :param toparty:指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，当touser为”@all”时忽略本参数
        :param totag:指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，，当touser为”@all”时忽略本参数
        :return:布尔值 是否成功
        """
        url = self.base_url + f"/message/send?access_token={self.token}"
        data = {
            "touser": touser,
            "toparty": toparty,
            "totag": totag,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": content
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        r = requests.post(url, json=data)
        errCode = r.json()["errcode"]
        if errCode == 0:
            return True
        elif errCode == 40014 or errCode == 42001 or errCode == 42007 or errCode == 42009:
            self.get_token()
            self.push(
                content=content,
                touser=touser,
                toparty=toparty,
                totag=totag)
        else:
            print(result["errmsg"])
            return False