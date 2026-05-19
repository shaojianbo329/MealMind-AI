import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MealMind AI",
    page_icon="🍱",
    layout="wide"
)

# =========================
# 数据读取
# =========================

@st.cache_data
def load_data():
    orders = pd.read_csv("data/mock_orders.csv")
    reviews = pd.read_csv("data/mock_reviews.csv")
    marketing = pd.read_csv("data/mock_marketing.csv")

    orders["order_date"] = pd.to_datetime(orders["order_date"])
    reviews["review_date"] = pd.to_datetime(reviews["review_date"])

    return orders, reviews, marketing


orders, reviews, marketing = load_data()

# =========================
# 页面标题
# =========================

st.title("🍱 MealMind AI｜AI 外卖商家经营助手")

st.markdown("""
MealMind AI 是一款面向外卖商家的智能经营分析与运营决策助手。  
本 Demo 使用模拟订单、评价和营销数据，展示经营看板、差评归因、营销分析与 AI 经营诊断流程。
""")

# =========================
# 侧边栏导航
# =========================

st.sidebar.title("功能导航")

page = st.sidebar.radio(
    "请选择功能模块",
    [
        "经营看板",
        "AI 经营诊断",
        "差评归因分析",
        "营销活动分析",
        "客服回复生成",
        "Agent 工作流"
    ]
)

# =========================
# 公共指标计算
# =========================

total_orders = len(orders)
total_revenue = orders["order_amount"].sum()
avg_order_amount = orders["order_amount"].mean()
avg_rating = orders["rating"].mean()
avg_delivery_minutes = orders["delivery_minutes"].mean()

negative_reviews = reviews[reviews["sentiment"] == "negative"]
negative_rate = len(negative_reviews) / len(reviews)

packaging_reviews = reviews[reviews["issue_type"] == "包装问题"]
packaging_rate = len(packaging_reviews) / len(reviews)

# =========================
# 1. 经营看板
# =========================

if page == "经营看板":
    st.header("经营看板")

    st.markdown("### 核心经营指标")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("订单量", total_orders, delta="-18%")
    col2.metric("营业额", f"¥{total_revenue:.0f}", delta="-12%")
    col3.metric("客单价", f"¥{avg_order_amount:.1f}", delta="+2%")
    col4.metric("平均评分", f"{avg_rating:.2f}", delta="-0.4")

    col5, col6, col7 = st.columns(3)

    col5.metric("平均配送时长", f"{avg_delivery_minutes:.1f} 分钟", delta="+8 分钟")
    col6.metric("差评率", f"{negative_rate:.1%}", delta="+23%")
    col7.metric("包装问题占比", f"{packaging_rate:.1%}", delta="+42%")

    st.warning("系统检测到：近 7 天差评率上升，包装类问题明显增加，可能影响用户下单转化。")

    st.markdown("### 每日订单趋势")

    daily_orders = orders.groupby("order_date").size().reset_index(name="order_count")
    st.line_chart(daily_orders.set_index("order_date"))

    st.markdown("### 菜品销量分布")

    item_sales = orders.groupby("item_name").size().reset_index(name="sales_count")
    st.bar_chart(item_sales.set_index("item_name"))

    st.markdown("### 经营看板说明")

    st.info("""
    经营看板用于帮助商家快速发现异常指标。  
    当前模拟数据中，汤类菜品的包装问题较突出，可能导致评分下降、差评上升和订单转化降低。
    """)

# =========================
# 2. AI 经营诊断
# =========================

elif page == "AI 经营诊断":
    st.header("AI 经营诊断")

    st.markdown("商家可以选择想要诊断的问题，系统会基于订单、评价和营销数据生成诊断报告。")

    question_type = st.selectbox(
        "请选择诊断问题",
        [
            "为什么我这周订单下降了？",
            "最近为什么差评变多了？",
            "这次营销活动为什么效果不好？",
            "哪些菜品最需要优先优化？"
        ]
    )

    if st.button("生成 AI 诊断报告"):
        st.subheader("AI 诊断报告")

        if question_type == "为什么我这周订单下降了？":
            st.markdown("### 一、异常现象")
            st.write("近 7 天订单量出现下降，同时平均评分降低、差评率上升。")

            st.markdown("### 二、关键证据")
            st.write("""
            1. 差评率上升，负面评价主要集中在包装问题；
            2. “汤洒了”“包装差”“包装不严实”等关键词高频出现；
            3. 低评分订单多集中在酸辣粉、牛肉汤饭、番茄肥牛汤等汤类菜品；
            4. 配送时长较长的订单更容易出现低评分。
            """)

            st.markdown("### 三、可能原因")
            st.write("""
            订单下降可能不是单一因素导致，而是由包装体验下降、配送时长增加、评分下降共同造成。
            """)

            st.markdown("### 四、优化建议")
            st.success("""
            1. 优先更换汤类菜品密封包装；
            2. 在商品页增加“汤粉分装”“密封包装”说明；
            3. 对近 30 天购买过汤类菜品的老客发放 5 元复购券；
            4. 针对包装类差评生成诚恳回复话术；
            5. 后续重点观察包装类差评占比、复购券使用率和转化率变化。
            """)

        elif question_type == "最近为什么差评变多了？":
            st.markdown("### 一、异常现象")
            st.write("近期差评主要集中在包装问题和配送问题。")

            st.markdown("### 二、差评归因")
            issue_counts = reviews.groupby("issue_type").size().reset_index(name="count")
            st.dataframe(issue_counts, use_container_width=True)

            st.markdown("### 三、关键证据")
            st.write("""
            高频负面关键词包括：汤洒了、包装差、包装不严实、配送慢、等太久。
            """)

            st.markdown("### 四、优化建议")
            st.success("""
            1. 优先优化汤类菜品包装；
            2. 高峰期适当延长预计送达时间，降低用户预期落差；
            3. 对包装类差评用户发放小额补偿券；
            4. 使用 AI 客服回复降低二次负面体验。
            """)

        elif question_type == "这次营销活动为什么效果不好？":
            st.markdown("### 一、异常现象")
            st.write("部分营销活动带来的订单增长有限，可能与活动目标用户和菜品体验不匹配有关。")

            st.markdown("### 二、营销数据")
            st.dataframe(marketing, use_container_width=True)

            st.markdown("### 三、可能原因")
            st.write("""
            1. 汤类菜品当前包装问题较多，不适合直接扩大促销；
            2. 部分活动面向全部用户，缺少新客和老客分层；
            3. 如果优惠力度较高但复购不足，可能导致 ROI 不稳定。
            """)

            st.markdown("### 四、优化建议")
            st.success("""
            1. 对新客使用新客券，提高首次转化；
            2. 对老客使用复购券，提升复购率；
            3. 暂缓大规模推广汤类菜品，先优化包装体验；
            4. 将评分稳定的炸鸡套餐作为短期引流菜品。
            """)

        elif question_type == "哪些菜品最需要优先优化？":
            st.markdown("### 一、问题菜品识别")

            issue_items = reviews[reviews["issue_type"] != "无"].groupby(
                ["item_name", "issue_type"]
            ).size().reset_index(name="issue_count")

            st.dataframe(issue_items, use_container_width=True)

            st.markdown("### 二、AI 判断")
            st.write("""
            从评价数据看，酸辣粉、牛肉汤饭、番茄肥牛汤等汤类菜品更容易出现包装洒漏问题。
            """)

            st.markdown("### 三、优化建议")
            st.success("""
            1. 优先优化汤类菜品包装；
            2. 对汤类菜品增加“汤粉分装”选项；
            3. 优化商品页描述，明确包装升级；
            4. 包装问题改善前，减少汤类菜品的大额促销。
            """)

        st.markdown("### 五、后续观察指标")

        st.info("""
        建议后续重点观察：订单量、转化率、评分、包装类差评占比、复购券使用率、营销 ROI。
        """)

# =========================
# 3. 差评归因分析
# =========================

elif page == "差评归因分析":
    st.header("差评归因分析")

    st.markdown("### 评价情绪分布")

    sentiment_counts = reviews.groupby("sentiment").size().reset_index(name="count")
    st.bar_chart(sentiment_counts.set_index("sentiment"))

    st.markdown("### 问题类型分布")

    issue_counts = reviews.groupby("issue_type").size().reset_index(name="count")
    st.bar_chart(issue_counts.set_index("issue_type"))

    st.markdown("### 负面评价列表")

    st.dataframe(
        negative_reviews[
            ["review_date", "item_name", "rating", "review_text", "issue_type", "keyword"]
        ],
        use_container_width=True
    )

    st.markdown("### AI 差评归因结论")

    st.info("""
    近 7 天差评主要集中在包装问题，尤其是汤类菜品。  
    高频问题包括：汤洒了、包装差、包装不严实、配送慢。  
    建议优先优化汤类菜品包装，并针对包装类差评生成诚恳回复话术。
    """)

# =========================
# 4. 营销活动分析
# =========================

elif page == "营销活动分析":
    st.header("营销活动分析")

    st.markdown("### 营销活动数据")

    st.dataframe(marketing, use_container_width=True)

    st.markdown("### 活动 ROI 对比")

    roi_data = marketing[["campaign_id", "campaign_type", "ROI"]]
    st.bar_chart(roi_data.set_index("campaign_id"))

    st.markdown("### AI 营销策略建议")

    st.success("""
    当前数据中，新客券和套餐组合表现相对较好。  
    但汤类菜品当前存在包装问题，不建议立即进行大规模促销。  

    建议：
    1. 保留新客券，用于提升新用户转化；
    2. 针对老客推出复购券，提升复购率；
    3. 将评分稳定的炸鸡套餐作为引流菜品；
    4. 先优化汤类包装，再推广汤类套餐。
    """)

# =========================
# 5. 客服回复生成
# =========================

elif page == "客服回复生成":
    st.header("客服回复生成")

    st.markdown("输入用户评价，系统会生成不同语气版本的回复话术。")

    default_review = "汤全洒了，包装太差了，等了很久才送到。"

    user_review = st.text_area("用户评价", default_review)

    issue_type = st.selectbox(
        "问题类型",
        ["包装问题", "配送问题", "口味问题", "价格问题", "服务问题"]
    )

    tone = st.selectbox(
        "回复语气",
        ["标准版", "诚恳版", "补偿引导版"]
    )

    if st.button("生成客服回复"):
        st.subheader("AI 回复建议")

        if tone == "标准版":
            reply = "非常抱歉给您带来了不好的用餐体验。关于您反馈的问题，我们已经记录，并会尽快优化相关流程。感谢您的反馈，也希望后续能为您提供更好的体验。"
        elif tone == "诚恳版":
            reply = "真的非常抱歉让您遇到这次不好的体验。您反馈的情况我们已经认真记录，后续会优先检查包装和出餐流程，尽量避免类似问题再次发生。感谢您指出问题，我们会认真改进。"
        else:
            reply = "非常抱歉给您带来了不便。关于您反馈的问题，我们已经记录并会尽快优化。您也可以通过平台订单页面联系我们，我们会根据实际情况协助处理。"

        st.code(reply, language="text")

        st.markdown("### 回复注意事项")
        st.warning("""
        - 不要直接指责用户或配送员；
        - 不要承诺平台外补偿；
        - 严重投诉建议引导用户通过平台订单渠道处理；
        - 包装类问题应同步进入经营优化待办。
        """)

# =========================
# 6. Agent 工作流
# =========================

elif page == "Agent 工作流":
    st.header("Agent 工作流")

    st.markdown("MealMind AI 通过多个 Agent 协作完成经营诊断。")

    st.markdown("""
```text
商家提出问题
↓
问题识别与任务拆解
↓
数据分析 Agent：判断订单、转化、评分等指标异常
↓
评价洞察 Agent：分析差评、关键词和问题菜品
↓
营销策略 Agent：生成优惠券、套餐和复购策略
↓
客服话术 Agent：生成评价回复和投诉安抚话术
↓
系统汇总为经营诊断报告
```
""")

    st.markdown("### Agent 分工")

    agent_table = pd.DataFrame({
        "Agent": ["数据分析 Agent", "评价洞察 Agent", "营销策略 Agent", "客服话术 Agent"],
        "输入": [
            "订单、流量、转化、评分数据",
            "用户评价、投诉、问题标签",
            "经营指标、菜品表现、营销数据",
            "用户评价、问题类型、商家语气"
        ],
        "输出": [
            "异常指标、关键证据、初步原因",
            "差评分类、高频关键词、问题菜品",
            "营销建议、适用用户、风险提示",
            "标准版、诚恳版、补偿引导版回复"
        ]
    })

    st.dataframe(agent_table, use_container_width=True)

    st.info("""
    当前 Demo 使用规则化逻辑模拟 Agent 输出。  
    后续可以接入 LLM API 和 RAG 知识库，实现动态 Agent 调用和平台规则检索。
    """)
