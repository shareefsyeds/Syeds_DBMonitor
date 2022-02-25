import requests
import json
import os
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'db_monitor.settings'

def send_ding_msg(content):
# The requested URL, WebHook address
    webhook = settings.DING_WEBHOOK
    is_send_ding_msg = settings.IS_SEND_DING_MSG

# build request header
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
}
#Build request data
    message ={

        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {

            "isAtAll": True
        }

    }
#Json request data encapsulation
    message_json = json.dumps(message)
    
    if is_send_ding_msg == 1:
#Send the request
        info = requests.post(url=webhook,data=message_json,headers=header) 
#Print the results returned
        print('Nailing the alarm sent：{}'.format(info.text))


if __name__=="__main__":
    content = 'The alarm test'
    send_ding_msg(content)