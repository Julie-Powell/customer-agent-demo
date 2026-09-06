import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from analysis.metric import analyze_metrics

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://zzzzz.dpdns.org/v1"
)


def generate_business_summary():
    # Python 先计算已经确认的业务数据
    metrics = analyze_metrics()

    prompt = f"""
你是一个客服业务信息中转 Agent。

你的任务不是创造数据，而是把已经计算确认的业务数据整理成简洁、准确的业务摘要。

请严格遵守：
1. 只能使用下面提供的数据。
2. 不允许编造数据。
3. 不要直接判断因果关系。
4. 如果需要进一步调查，请明确写成“待验证事项”。
5. 需要结合具体数据进行描述。

已确认的业务数据：
{metrics}

请严格按照下面的 JSON 格式输出，不要输出任何其他文字：

{{
    "业务摘要": "结合具体数据，用1到2句话说明当前客服业务发生了什么变化",
    "异常情况": [
        "结合具体指标描述异常"
    ],
    "待验证事项": [
        "结合当前数据提出需要进一步查看的事项"
    ]
}}
"""

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    result = generate_business_summary()

    print("\n========== AI业务摘要 ==========")

    print("\n【业务摘要】")
    print(result["业务摘要"])

    print("\n【异常情况】")
    for item in result["异常情况"]:
        print(f"- {item}")

    print("\n【待验证事项】")
    for item in result["待验证事项"]:
        print(f"- {item}")