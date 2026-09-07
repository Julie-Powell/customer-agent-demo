from agent.deepseek_agent import generate_business_summary
from push.notify import send_notification
import streamlit as st
from analysis.metric import analyze_metrics
from analysis.trend import analyze_trend


# =========================
# 页面标题
# =========================

st.title("客服业务信息中转 Agent")

st.write("客服业务监测与信息中转系统")


# =========================
# 获取业务指标
# =========================

metrics = analyze_metrics()
trend = analyze_trend()

# =========================
# 业务指标
# =========================

st.subheader("📊 今日业务指标")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "咨询量",
        metrics["咨询量"],
        f'{metrics["咨询量变化"]}%'
    )


with col2:

    st.metric(
        "满意度",
        f'{metrics["满意度"]}%',
        f'{metrics["满意度变化"]} 个百分点'
    )


with col3:

    st.metric(
        "平均响应时间",
        f'{metrics["平均响应时间"]} 分钟'
    )



# =========================
# 异常情况
# =========================

st.subheader("⚠️ 异常情况")


if metrics["异常"]:

    for item in metrics["异常"]:
        st.warning(item)

else:

    st.success("今日业务正常，无异常")


# =========================
# 趋势分析
# =========================

st.divider()

st.subheader("📈 业务趋势")


st.write("咨询量趋势")

st.line_chart(
    trend.set_index("date")["consult_count"]
)


st.write("满意度趋势")

st.line_chart(
    trend.set_index("date")["satisfaction"]
)


st.write("响应时间趋势")

st.line_chart(
    trend.set_index("date")["response_time"]
)
# =========================
# AI Agent
# =========================

st.divider()

st.subheader("🤖 AI业务助手")


# 保存AI结果
if "ai_result" not in st.session_state:

    st.session_state.ai_result = None



# --------
# 生成AI摘要按钮
# --------

if st.button("生成 AI 业务摘要"):

    with st.spinner("DeepSeek 正在分析业务数据..."):

        result = generate_business_summary()

        st.session_state.ai_result = result



# 展示AI结果

if st.session_state.ai_result:


    result = st.session_state.ai_result


    st.markdown("### 业务摘要")

    st.write(
        result["业务摘要"]
    )


    st.markdown("### 异常情况")


    for item in result["异常情况"]:

        st.warning(item)



    st.markdown("### 待验证事项")


    for item in result["待验证事项"]:

        st.info(item)



    st.divider()


    # --------
    # 飞书按钮
    # --------

    if st.button("📤 发送飞书提醒"):

        with st.spinner("正在发送飞书消息..."):

            send_notification()


        st.success("已发送到飞书群")


else:

    st.info("请先生成 AI 业务摘要")