import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from analysis.metric import analyze_metrics
from analysis.trend import analyze_trend
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://zzzzz.dpdns.org/v1"
)


def generate_business_summary():
    # Python 先计算已经确认的业务数据
    metrics = analyze_metrics()
    trend = analyze_trend()

    prompt = f"""
你是一个客服业务信息中转 Agent。

你的任务不是创造数据，而是把已经计算确认的业务数据整理成简洁、准确的业务摘要。
你的职责是整理已确认数据，帮助业务人员发现需要关注的问题。
请严格遵守：
1. 只能使用下面提供的数据。
2. 不允许编造数据。
3. 不要直接判断因果关系。
4. 如果需要进一步调查，请明确写成“待验证事项”。
5. 需要结合具体数据进行描述。

已确认的业务数据：

当前指标：
{metrics}


趋势数据：
{trend}

请严格按照下面的 JSON 格式输出，不要输出任何其他文字：

请严格按照下面 JSON 格式输出，不要输出任何其他文字：

{{
    "业务摘要": "结合当前指标和趋势，用1到2句话描述客服业务整体变化，只描述事实，不推测原因",

    "异常情况": [
        "结合具体指标和趋势描述异常，例如增长、下降、波动"
    ],

    "待验证事项": [
        "根据异常和趋势提出下一步需要查看的数据方向，不得直接给出原因"
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