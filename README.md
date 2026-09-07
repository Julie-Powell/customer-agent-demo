# 客服业务信息中转 Agent


## 项目介绍

客服业务信息中转 Agent 是一个基于业务数据分析、LLM 智能推理和消息推送的 AI Agent 系统。

系统自动读取客服业务指标，分析咨询量、满意度、响应时间等关键指标变化，通过 DeepSeek 生成业务摘要和异常分析，并通过飞书机器人自动通知业务人员。


## 解决的问题

传统客服运营过程中：

- 需要人工查看数据报表
- 难以及时发现业务异常
- 数据变化缺少原因分析
- 信息传递依赖人工


本项目通过 Agent 实现：

数据 → 分析 → AI判断 → 信息推送


## 系统架构
客服业务数据
  ↓
SQLite 数据库
  ↓
指标分析模块
analysis/metric.py
  ↓
DeepSeek Agent
agent/deepseek_agent.py
  ↓
Streamlit 飞书机器人
业务看板 自动提醒


## 核心功能


### 1. 业务指标监控

自动计算：

- 咨询量
- 满意度
- 平均响应时间
- 环比变化


### 2. AI业务分析

调用 DeepSeek：

自动生成：

- 业务摘要
- 异常情况
- 待验证事项


### 3. 自动消息推送

通过飞书 Webhook：

将异常情况自动发送给业务人员。


## 技术栈


- Python
- SQLite
- Pandas
- Streamlit
- DeepSeek API
- 飞书机器人 Webhook


## Demo效果


业务数据：
咨询量：2120
增长：24.7%

满意度：82.5%
下降：3.5个百分点

平均响应时间：
14.5分钟


AI分析：
业务摘要：

客服咨询量明显上涨，同时满意度下降。

待验证事项：

1.是否存在渠道活动导致咨询增加
2.是否存在响应能力不足


## 项目目录
customer-agent-demo

├── agent
│ └── deepseek_agent.py

├── analysis
│ ├── metric.py
│ └── read_data.py

├── database
│ └── customer.db

├── push
│ └── notify.py

├── data
│ └── customer.csv

├── app.py

└── README.md


## 后续规划

- 接入真实业务数据库
- 增加历史趋势分析
- 增加多业务Agent协作
- 支持更多消息渠道
