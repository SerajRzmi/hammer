import requests
 
def hammer_alert(date, symbol, hammer_type, id):
    url = "https://api.telegram.org/bot5127440250%3AAAET7ljlaYJzmlPsSY_oRPRAijeVFA6PKyA/sendMessage"

    payload = {
        "text": str(date) + '--' + symbol + '--' +str(hammer_type),
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "chat_id": str(id)
        }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)

