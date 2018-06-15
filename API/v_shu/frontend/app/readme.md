使用说明：
1.运行环境：
 需要 python3 + mogodb数据库

2.使用方法：
使用时先启动mongodb服务器，然后运行app_run.py程序，此时会在输出窗口有一个链接，点击该链接即可进入聊天窗口界面，
在该界面上输入问题，点击发送（或者按enter键），机器人即可有相应的回答再此显示。
每运行一次，问答对话都将会被保存在mongdb数据库flask_database中，此数据库会在运行程序时自动生成。

3.程序说明：
app_run.py是运行程序，修改时只需将自己机器人的查询结果赋值给result变量即可，即"result = get_data(query)"
mong_database.py 是mongodb的配置，包括ip,端口，以及数据库flask_database等。