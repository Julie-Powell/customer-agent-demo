import requests
from agent.deepseek_agent import generate_business_summary


def send_notification():

    result = generate_business_summary()


    # 没有异常，不推送
    if not result["异常情况"]:
        print("今日无异常，无需推送")
        return


    message = f"""
【客服业务日报】

业务摘要：
{result["业务摘要"]}


异常情况：
"""


    for item in result["异常情况"]:
        message += f"\n- {item}"


    message += "\n\n待验证事项："


    for item in result["待验证事项"]:
        message += f"\n- {item}"


    # 飞书推送部分必须在这里
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/765c1877-da99-4a4c-9d48-580f40d42d48"


    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }


    response = requests.post(
        webhook_url,
        json=data
    )


    print(response.text)



if __name__ == "__main__":

    send_notification()