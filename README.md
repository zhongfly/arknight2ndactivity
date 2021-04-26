# arknight2ndactivity
明日方舟2周年庆典筹备活动网页每日任务

# 使用简介
1.打开活动网页，登录账号，按F12打开开发者工具--》刷新网页--》按如下步骤，找到cookie，复制cookie：后的内容
![获得cookie](https://user-images.githubusercontent.com/11155705/115988114-c3276000-a5ea-11eb-9e41-50fc16e701dc.png)

2.“Settings” --》“Secrets” 中点击New repository secret，Name填"COOKIES"（不含引号），Value填步骤1得到的cookie内容。如果有多个账号，按如下格式：
  ```
  用户1的cookie
  用户2的cookie
  (多个账户继续加在后面）
  ```
3.进入"Actions" --》"Arknight activity"，点击右边的"Run workflow"即可第一次启动

4.第一次启动后，脚本会每天6:00、18:00自动执行，不需要再次手动执行。

# 推送结果
## Server酱·Turbo版
https://sct.ftqq.com/

“Settings” --》“Secrets” 中点击New repository secret，Name填"SCT_SCENDKEY"（不含引号），Value填你申请的sendkey

## 邮箱推送
“Settings” --》“Secrets” 中点击New repository secret，Name填"EMAIL"（不含引号），Value填接收消息的邮箱

## telegram bot
“Settings” --》“Secrets” 中点击New repository secret，Name填"TELEGRAM"（不含引号），Value按以下格式
```
telegram_bot_token,telegram_bot_chatid
```
注意是英文逗号！

## 微信模板消息推送
1.[申请测试号](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login )，记录“测试号信息”的appID、appsecret

2.在测试号管理面板中“测试号二维码”，扫码关注，记录用户列表中你的微信号

3.在测试号管理面板中“模板消息接口”-“新增测试模板”，标题任意，模板内容输入“{{content.DATA}}”（不含双引号），记录模板ID

4.Github项目中“Settings” --》“Secrets” 中点击New repository secret，Name填"WX_TEMPLATE"（不含引号），Value按以下格式
```
appID,appsecret,模板ID,你的微信号
```
注意是英文逗号！

## 企业微信应用消息推送
1.申请[企业微信](https://work.weixin.qq.com/) 

2.创建应用:注册成功后，点「管理企业」进入管理界面，选择「应用管理」 → 「自建」 → 「创建应用」

3.应用名称任意，可见范围选择公司名。

4.创建完成后进入应用详情页，可以得到应用ID( agentid )，应用Secret( secret )，复制

5.获取企业ID：进入「我的企业」页面，拉到最下边，可以看到企业ID，复制

6.进入「我的企业」 → 「微信插件」，拉到下边扫描二维码，关注

4.Github项目中“Settings” --》“Secrets” 中点击New repository secret，Name填"WX_QY"（不含引号），Value按以下格式
```
企业ID,应用Secret（secret）,应用ID（agentid）
```
注意是英文逗号！