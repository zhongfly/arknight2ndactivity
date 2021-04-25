# -*- encoding: utf-8 -*-
import os

import requests


class activity:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    }
    base_url = "https://ak.hypergryph.com/activity/preparation/activity/"
    is_share = False
    roll_chance = 2

    def __init__(self, cookies):
        self.cookies = cookies

    def get_userinfo(self):
        r = requests.get(
            self.base_url + "userInfo",
            headers=self.headers,
            cookies=self.cookies)
        if r.status_code == 200:
            userinfo = r.json()["data"]
            self.roll_chance = userinfo["rollChance"]
            self.is_share = not userinfo["share"]
            return userinfo
        else:
            raise Exception("get_userinfo Error! status_code:" +
                            str(r.status_code) + "\n" + r.text)

    def share(self):
        jsondata = {"method": 1}
        r = requests.post(
            self.base_url + "share",
            json=jsondata,
            headers=self.headers,
            cookies=self.cookies)
        # 每天第一次签到返回200，之后再次签到返回201
        if r.status_code == 200 or r.status_code == 201:
            self.is_share = True
            result = r.json()["data"]["todayFirst"]
            if result:
                print("本日首次分享活动页面，助力收集「原料数」*10")
            else:
                print("本日已经分享过活动页面了")
            return result
        else:
            raise Exception("share Error! status_code:" +
                            str(r.status_code) + "\n" + r.text)

    def roll(self):
        jsondata = {}
        r = requests.post(
            self.base_url + "roll",
            json=jsondata,
            headers=self.headers,
            cookies=self.cookies)
        if r.status_code == 200 or r.status_code == 201:
            data = r.json()["data"]
            coin = data["coin"]
            print(f"成功收集一个「调色奶油袋」，获得美味值：{coin}")
            self.roll_chance -= 1
            return coin
        elif r.status_code == 400:
            #{"statusCode":400,"message":"今日获取机会已耗尽","error":"Bad Request"}
            self.roll_chance = 0
        else:
            raise Exception("roll Error! status_code:" +
                            str(r.status_code) + "\n" + r.text)

    def daily(self):
        self.get_userinfo()
        while self.is_share == False:
            self.share()
        while self.roll_chance > 0:
            self.roll()
        info = self.get_userinfo()
        share_str = "今日尚未分享活动页面" if info["share"] else "今日已分享活动页面"
        roll_str = f"今日已收集「调色奶油袋」{2-info['rollChance']}个"
        result = f"uid为{info['uid']}的玩家活动参与情况：{share_str}，{roll_str}，目前拥有「美味值」：{info['remainCoin']}，助力收集「原料数」：{info['totalPoint']}"
        print(result)
        return result

    def sct(sendkey,content):
        data = {"title":"【明日方舟】庆典筹备计划每日任务","desp":content}
        r = requests.post(f"https://sctapi.ftqq.com/{sendkey}.send",data=data)

def push(content):
    def sct(sendkey,content):
        data = {"title":"【明日方舟】庆典筹备计划每日任务","desp":content}
        r = requests.post(f"https://sctapi.ftqq.com/{sendkey}.send",data=data)

    def email(target,content):
        data = {"title": "【明日方舟】庆典筹备计划每日任务", "text": content,"to":target}
        r = requests.post("https://email.berfen.com/api",data=data)

    def telegram(keys,content):
        token,chat_id = keys.split(",")
        data = {"text": content,"chat_id":chat_id}
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage")

    sct_sendkey: str = os.environ.get('SCT_SCENDKEY', None)
    if sct_sendkey:
        sct(sct_sendkey,content)
        print("已使用Server酱·Turbo版进行推送")
    email_target: str = os.environ.get('EMAIL', None)
    if email_target:
        email(email_target,content)
        print("已使用邮箱推送")
    telegram_str: str = os.environ.get('TELEGRAM', None)
    if telegram_str:
        telegram(telegram_str,content)
        print("telegram")

def cookie_str2dict(cookies_str: str):
    cookies_dict = {}
    if cookies_str != "":
        for line in cookies_str.split(";"):
            if line == "":
                break
            key, value = line.strip().split("=", 1)
            cookies_dict[key] = value
    return cookies_dict


def main():
    users: str = os.environ.get('COOKIES', None)
    if users:
        for i, cookie_str in enumerate(users.split("\n")):
            a = activity(cookie_str2dict(cookie_str))
            result = a.daily()
            push(result)
    else:
        print("未找到用户信息")

if __name__ == "__main__":
    main()