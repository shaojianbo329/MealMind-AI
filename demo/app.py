import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MealMind AI",
    page_icon="🍱",
    layout="wide"
)

st.title("🍱 MealMind AI｜AI 外卖商家经营助手")

st.markdown("""
MealMind AI 是一款面向外卖商家的智能经营分析与运营决策助手。  
本 Demo 使用模拟订单、评价和营销数据，展示经营看板、差评归因、营销效果和 AI 经营诊断流程。
""")

# 读取数据
orders = pd.read_csv("data/mock_orders.csv")
reviews = pd.read_csv("data/mock_reviews.csv")
marketing = pd.read_csv("data/mock_marketing.csv")

# 数据预处理
orders["order_date"] = pd.to_datetime(orders["order_date"])
reviews["review_date"] = pd.to_datetime(reviews["review_date"])

# 侧边栏
st.sidebar.title("功能导航")
page = st.sidebar.radio(
    "请选择功能模块",
    ["经营看板", "差评归因分析", "营销活动分析", "AI 经营诊断示例"]
)

# =========================
# 1. 经营看板
# =========================
if page == "经营看板":
    st.header("经营看板")

    total_orders = len(orders)
    total_revenue = orders["order_amount"].sum()
    avg_order_amount = orders["order_amount"].mean()
    avg_rating = orders["rating"].mean()
    avg_delivery_minutes = orders["delivery_minutes"].mean()
    negative_reviews = len(reviews[reviews["sentiment"] == "negative"])
    negative_rate = negative_reviews / len(reviews)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("订单量", total_orders)
    col2.metric("营业额", f"¥{total_revenue:.0f}")
    col3.metric("客单价", f"¥{avg_order_amount:.1f}")
    col4.metric("平均评分", f"{avg_rating:.2f}")

    col5, col6 = st.columns(2)
    col5.metric("平均配送时长", f"{avg_delivery_minutes:.1f} 分钟")
    col6.metric("差评率", f"{negative_rate:.1%}")

    st.subheader("每日订单趋势")
    daily_orders = orders.groupby("order_date").size().reset_index(name="order_count")
    st.line_chart(daily_orders.set_index("order_date"))

    st.subheader("菜品销量")
    item_sales = orders.groupby("item_name").size().reset_index(name="sales_count")
    st.bar_chart(item_sales.set_index("item_name"))

# =========================
# 2. 差评归因分析
# =========================
elif page == "差评归因分析":
    st.header("差评归因分析")

    issue_counts = reviews.groupby("issue_type").size().reset_index(name="count")
    st.subheader("评价问题类型分布")
    st.bar_chart(issue_counts.set_index("issue_type"))

    negative_reviews_df = reviews[reviews["sentiment"] == "negative"]

    st.subheader("负面评价列表")
    st.dataframe(
        negative_reviews_df[
            ["review_date", "item_name", "rating", "review_text", "issue_type", "keyword"]
        ],
        use_container_width=True
    )

    st.subheader("AI 差评归因结论示例")
    st.info("""
    近 7 天差评主要集中在包装问题，尤其是汤类菜品如“番茄肥牛汤”“牛肉汤饭”“酸辣粉”。

    主要问题包括：
    1. 汤品洒漏；
    2. 包装不严实；
    3. 配送时间较长导致用户体验下降。

    建议优先优化汤类菜品包装，并在商品页增加“汤粉分装”“密封包装”说明。
    """)

# =========================
# 3. 营销活动分析
# =========================
elif page == "营销活动分析":
    st.header("营销活动分析")

    st.subheader("营销活动数据")
    st.dataframe(marketing, use_container_width=True)

    st.subheader("活动 ROI 对比")
    marketing_roi = marketing[["campaign_id", "campaign_type", "ROI"]]
    st.bar_chart(marketing_roi.set_index("campaign_id"))

    st.subheader("AI 营销建议示例")
    st.success("""
    当前活动中，新客券和套餐组合表现较好。

    建议：
    1. 继续保留新客券，用于提升新用户转化；
    2. 针对老客推出复购券，提升复购率；
    3. 对汤类菜品暂缓大规模促销，先优化包装体验；
    4. 将“炸鸡套餐”作为稳定高评分菜品，用于引流活动。
    """)

# =========================
# 4. AI 经营诊断示例
# =========================
elif page == "AI 经营诊断示例":
    st.header("AI 经营诊断示例")

    user_question = st.text_input(
        "请输入商家经营问题",
        "为什么我这周订单下降了？"
    )

    if st.button("生成 AI 诊断报告"):
        st.subheader("AI 诊断报告")

        st.markdown("### 一、异常现象")
        st.write("近 7 天订单表现出现波动，部分汤类菜品评分下降，差评率上升。")

        st.markdown("### 二、关键证据")
        st.write("""
        1. 负面评价主要集中在包装问题；
        2. “汤洒了”“包装差”“包装不严实”等关键词高频出现；
        3. 差评主要集中在酸辣粉、牛肉汤饭、番茄肥牛汤等汤类菜品；
        4. 配送时长较长的订单更容易出现低评分。
        """)

        st.markdown("### 三、可能原因")
        st.write("""
        订单下降可能不是单一因素导致，而是由包装体验下降、配送时长增加和用户评分下降共同造成。
        """)

        st.markdown("### 四、优化建议")
        st.write("""
        1. 优先更换汤类菜品的密封包装；
        2. 在商品页增加“汤粉分装”“密封包装”说明；
        3. 针对近 30 天购买过汤类菜品的老客发放 5 元复购券；
        4. 针对包装类差评生成诚恳回复话术；
        5. 后续重点观察包装类差评占比、复购券使用率和转化率变化。
        """)

        st.markdown("### 五、客服回复示例")
        st.code(
            "非常抱歉给您带来了不好的用餐体验。关于您反馈的汤品洒漏问题，我们已经记录并会立即优化汤类菜品的密封包装，同时加强高峰期出餐和配送衔接。感谢您的反馈，也希望后续能给您带来更好的体验。",
            language="text"
        )
