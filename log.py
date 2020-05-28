import json
import requests

CORP_ID = "ww925c7744e023b5f2"
SECRET = "XkZmRzGdersPoNTwXUhs1uyfjN6cffbwni8xP94Lm9"

class Log:
    def __init__(self, message):
        res = requests.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(
            CORP_ID, SECRET)).json()
        print(res)
        token = res["access_token"]

        req_data = {
            "touser" : "dbw",
            "msgtype" : "text",
            "agentid" : 1000002,
            "text" : {
                "content" : message
            }
        }
        res = requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
                            + token, json.dumps(req_data))
        print(res.json())

if __name__ == "__main__":
    Log("服务器爬虫已启动！")
