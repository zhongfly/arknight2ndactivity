# arknight2ndactivity
明日方舟2周年庆典筹备活动网页每日任务

# 使用简介
1.打开活动网页，登录账号，按F12打开开发者工具--》刷新网页--》按如下步骤，找到cookie，复制cookie：后的内容
![获得cookie](https://i.loli.net/2021/04/25/7qQgxRalCeEXLvN.png)

2. “Settings” --》“Secrets” 中点击New repository secret，Name填"COOKIES"（不含引号），Value填步骤1得到的cookie内容。如果有多个账号，按如下格式：
  ```
  用户1的cookie
  用户2的cookie
  (多个账户继续加在后面）
  ```
3.进入"Actions" --》"Arknight activity"，点击右边的"Run workflow"即可第一次启动

4.第一次启动后，脚本会每天6:00、18:00自动执行，不需要再次手动执行。
