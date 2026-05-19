import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="MealMind AI",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded",
)


MODE_CONFIG = {
    "Boardroom Mode": {
        "label": "董事会视图",
        "eyebrow": "Brand System · Executive Narrative",
        "headline": "让每一家餐饮品牌，都拥有自己的 AI 经营团队。",
        "description": "MealMind AI 将订单、评价、营销和客服动作整合进统一界面，帮助门店和品牌团队更快识别风险、发现增长机会，并把经营判断转成可执行动作。",
        "accent": "#1d4ed8",
        "secondary": "#0f766e",
        "warning": "#d97706",
    },
    "Recovery Mode": {
        "label": "口碑修复",
        "eyebrow": "Brand System · Recovery Narrative",
        "headline": "把差评、履约和安抚动作，整合成一套可持续的口碑恢复系统。",
        "description": "这一模式聚焦评分修复、用户回应和商品治理，帮助商家用更有节奏的方式压降差评、修复体验并恢复复购信心。",
        "accent": "#0f766e",
        "secondary": "#1d4ed8",
        "warning": "#e11d48",
    },
    "Growth Mode": {
        "label": "增长实验",
        "eyebrow": "Brand System · Growth Narrative",
        "headline": "把拉新、复购和品类策略，放进同一套可复盘的增长实验框架。",
        "description": "这一模式强调投放效率、品类结构与复购表现之间的关系，适合展示商家如何在稳定体验之后持续放大增长。",
        "accent": "#7c3aed",
        "secondary": "#1d4ed8",
        "warning": "#f97316",
    },
}

CAMPAIGN_LABELS = {
    "new_user_coupon": "新客立减券",
    "repeat_user_coupon": "老客复购券",
    "full_discount": "满减活动",
    "combo_package": "套餐组合",
}


@st.cache_data
def load_data():
    orders = pd.read_csv("data/mock_orders.csv")
    reviews = pd.read_csv("data/mock_reviews.csv")
    marketing = pd.read_csv("data/mock_marketing.csv")

    orders["order_date"] = pd.to_datetime(orders["order_date"])
    reviews["review_date"] = pd.to_datetime(reviews["review_date"])
    marketing["start_date"] = pd.to_datetime(marketing["start_date"])
    marketing["end_date"] = pd.to_datetime(marketing["end_date"])
    marketing["expected_lift"] = (
        marketing["expected_order_increase"].str.rstrip("%").astype(float)
    )
    marketing["actual_lift"] = (
        marketing["actual_order_increase"].str.rstrip("%").astype(float)
    )
    marketing["item_list"] = marketing["items_involved"].str.split("+")
    marketing["campaign_label"] = marketing["campaign_type"].map(CAMPAIGN_LABELS).fillna(
        marketing["campaign_type"]
    )
    orders["hour"] = pd.to_datetime(orders["order_time"], format="%H:%M").dt.hour

    return orders, reviews, marketing


def inject_styles(accent, secondary, warning):
    st.markdown(
        f"""
        <style>
        :root {{
            --bg-top: #f6efe6;
            --bg-bottom: #eef5fb;
            --ink: #0f2337;
            --muted: #5b7085;
            --soft-line: rgba(148, 163, 184, 0.16);
            --glass: rgba(255, 255, 255, 0.72);
            --glass-strong: rgba(255, 255, 255, 0.86);
            --accent: {accent};
            --secondary: {secondary};
            --warning: {warning};
            --rose: #e11d48;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 0% 0%, rgba(249, 115, 22, 0.16), transparent 24%),
                radial-gradient(circle at 100% 0%, rgba(29, 78, 216, 0.16), transparent 26%),
                radial-gradient(circle at 75% 80%, rgba(15, 118, 110, 0.12), transparent 24%),
                linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 56%, #f4f8fc 100%);
            color: var(--ink);
            font-family: "Avenir Next", "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
        }}

        .block-container {{
            max-width: 1440px;
            padding-top: 1.35rem;
            padding-bottom: 3rem;
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(9, 18, 33, 0.98) 0%, rgba(15, 44, 63, 0.98) 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.07);
        }}

        [data-testid="stSidebar"] * {{
            color: #f8fafc !important;
        }}

        [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] .stDateInput > div > div,
        [data-testid="stSidebar"] .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.10);
        }}

        .brand-header {{
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: stretch;
            margin-bottom: 1rem;
        }}

        .brand-lockup {{
            flex: 1.45;
            position: relative;
            overflow: hidden;
            border-radius: 32px;
            padding: 2rem 2.1rem;
            color: #ffffff;
            background:
                linear-gradient(140deg, rgba(7, 20, 32, 0.98) 0%, rgba(10, 74, 106, 0.96) 44%, rgba(17, 24, 39, 0.94) 100%);
            box-shadow: 0 28px 90px rgba(15, 23, 42, 0.18);
        }}

        .brand-lockup::before {{
            content: "";
            position: absolute;
            right: -100px;
            top: -110px;
            width: 320px;
            height: 320px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255,255,255,0.14) 0%, rgba(255,255,255,0.02) 70%, transparent 72%);
        }}

        .brand-lockup::after {{
            content: "";
            position: absolute;
            left: 46%;
            bottom: -120px;
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.06);
        }}

        .eyebrow {{
            display: inline-flex;
            gap: 0.45rem;
            align-items: center;
            padding: 0.36rem 0.8rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.12);
            color: rgba(255, 255, 255, 0.92);
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.9rem;
        }}

        .brand-row {{
            display: flex;
            gap: 1rem;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .brand-mark {{
            width: 74px;
            height: 74px;
            border-radius: 24px;
            background:
                linear-gradient(145deg, rgba(255,255,255,0.24), rgba(255,255,255,0.04));
            border: 1px solid rgba(255, 255, 255, 0.18);
            display: grid;
            place-items: center;
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.06em;
        }}

        .brand-name {{
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: -0.04em;
        }}

        .brand-subtitle {{
            color: rgba(255, 255, 255, 0.72);
            font-size: 0.92rem;
            margin-top: 0.1rem;
        }}

        .brand-lockup h1 {{
            margin: 0;
            max-width: 860px;
            font-size: 2.72rem;
            line-height: 1.03;
            letter-spacing: -0.06em;
        }}

        .brand-lockup p {{
            max-width: 760px;
            margin: 0.95rem 0 1.18rem;
            line-height: 1.8;
            color: rgba(255, 255, 255, 0.84);
            font-size: 1rem;
        }}

        .brand-pill-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
        }}

        .brand-pill {{
            padding: 0.58rem 0.84rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: rgba(255, 255, 255, 0.94);
            font-size: 0.84rem;
        }}

        .brand-pill strong {{
            color: #ffffff;
        }}

        .brand-radar {{
            flex: 0.92;
            border-radius: 32px;
            padding: 1.4rem;
            background: var(--glass);
            border: 1px solid var(--soft-line);
            box-shadow: 0 18px 54px rgba(15, 23, 42, 0.08);
            backdrop-filter: blur(20px);
        }}

        .brand-radar h3 {{
            margin: 0.45rem 0 0.4rem;
            font-size: 1.46rem;
            letter-spacing: -0.04em;
            color: var(--ink);
        }}

        .brand-radar p {{
            margin: 0;
            color: var(--muted);
            line-height: 1.72;
        }}

        .score-wrap {{
            display: grid;
            grid-template-columns: 118px 1fr;
            gap: 1rem;
            align-items: center;
            margin-top: 1.15rem;
        }}

        .score-ring {{
            width: 118px;
            height: 118px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            background: conic-gradient(var(--secondary) 0%, var(--accent) 48%, var(--warning) 80%, rgba(255,255,255,0.12) 80%);
        }}

        .score-inner {{
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.92);
            color: var(--ink);
            display: grid;
            place-items: center;
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.05em;
        }}

        .score-notes p {{
            margin: 0 0 0.3rem;
        }}

        .section-kicker {{
            margin-top: 0.85rem;
            margin-bottom: 0.35rem;
            color: var(--warning);
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .section-title {{
            margin: 0 0 0.95rem;
            color: var(--ink);
            font-size: 1.68rem;
            letter-spacing: -0.05em;
        }}

        .metric-card,
        .glass-card,
        .signal-card,
        .timeline-card,
        .reply-card,
        .review-card,
        .workflow-step,
        .notice-card,
        .manifesto-card {{
            border: 1px solid var(--soft-line);
            box-shadow: 0 18px 48px rgba(15, 23, 42, 0.07);
        }}

        .metric-card {{
            min-height: 132px;
            border-radius: 24px;
            padding: 1.12rem 1.16rem;
            background: var(--glass-strong);
        }}

        .metric-label {{
            color: var(--muted);
            font-size: 0.88rem;
            margin-bottom: 0.64rem;
        }}

        .metric-value {{
            color: var(--ink);
            font-size: 1.96rem;
            font-weight: 800;
            letter-spacing: -0.05em;
            line-height: 1;
            margin-bottom: 0.42rem;
        }}

        .metric-delta {{
            display: inline-block;
            padding: 0.28rem 0.58rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
        }}

        .delta-good {{
            color: #0f766e;
            background: rgba(20, 184, 166, 0.14);
        }}

        .delta-warn {{
            color: #b45309;
            background: rgba(245, 158, 11, 0.16);
        }}

        .delta-bad {{
            color: #be123c;
            background: rgba(244, 63, 94, 0.14);
        }}

        .notice-card {{
            padding: 1rem 1.08rem;
            border-radius: 22px;
            background: linear-gradient(135deg, rgba(254, 243, 199, 0.46), rgba(255, 255, 255, 0.82));
            color: #6b4f00;
        }}

        .manifesto-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 0.65rem;
            margin-bottom: 0.4rem;
        }}

        .trust-strip {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin: 1rem 0 0.5rem;
        }}

        .trust-chip {{
            padding: 0.72rem 0.92rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid var(--soft-line);
            color: var(--ink);
            font-size: 0.88rem;
            font-weight: 700;
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
        }}

        .feature-card {{
            border-radius: 28px;
            padding: 1.2rem 1.2rem 1.15rem;
            background: var(--glass);
            border: 1px solid var(--soft-line);
            box-shadow: 0 18px 48px rgba(15, 23, 42, 0.07);
            backdrop-filter: blur(20px);
            height: 100%;
        }}

        .feature-card h4 {{
            margin: 0.2rem 0 0.55rem;
            color: var(--ink);
            font-size: 1.1rem;
            letter-spacing: -0.03em;
        }}

        .feature-card p,
        .feature-card li {{
            color: #476175;
            font-size: 0.93rem;
            line-height: 1.72;
        }}

        .feature-card ul {{
            margin: 0.45rem 0 0;
            padding-left: 1.1rem;
        }}

        .feature-badge {{
            display: inline-block;
            padding: 0.28rem 0.58rem;
            border-radius: 999px;
            background: rgba(29, 78, 216, 0.10);
            color: var(--accent);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}

        .cta-banner {{
            margin-top: 1rem;
            padding: 1.35rem 1.4rem;
            border-radius: 30px;
            background:
                linear-gradient(135deg, rgba(15, 44, 63, 0.98) 0%, rgba(29, 78, 216, 0.94) 100%);
            color: #ffffff;
            box-shadow: 0 24px 64px rgba(15, 23, 42, 0.16);
        }}

        .cta-banner h3 {{
            margin: 0 0 0.5rem;
            font-size: 1.55rem;
            letter-spacing: -0.04em;
        }}

        .cta-banner p {{
            margin: 0;
            color: rgba(255, 255, 255, 0.84);
            line-height: 1.76;
            max-width: 900px;
        }}

        .manifesto-card,
        .glass-card,
        .signal-card,
        .reply-card,
        .timeline-card {{
            border-radius: 28px;
            background: var(--glass);
            backdrop-filter: blur(20px);
            padding: 1.18rem 1.22rem;
            height: 100%;
        }}

        .manifesto-card h4,
        .glass-card h4,
        .signal-card h4,
        .reply-card h4,
        .timeline-card h4 {{
            margin: 0 0 0.6rem;
            color: var(--ink);
            font-size: 1.04rem;
        }}

        .manifesto-card p,
        .glass-card p,
        .glass-card li,
        .signal-card p,
        .signal-card li,
        .reply-card p,
        .timeline-card p {{
            color: #476175;
            font-size: 0.93rem;
            line-height: 1.76;
        }}

        .glass-card ul,
        .signal-card ul {{
            margin: 0.45rem 0 0;
            padding-left: 1.1rem;
        }}

        .review-card {{
            border-radius: 24px;
            padding: 1rem 1.06rem;
            background: rgba(255, 255, 255, 0.86);
            margin-bottom: 0.82rem;
        }}

        .review-meta {{
            display: flex;
            justify-content: space-between;
            gap: 0.7rem;
            color: var(--muted);
            font-size: 0.82rem;
            margin-bottom: 0.5rem;
        }}

        .tag {{
            display: inline-block;
            margin-top: 0.3rem;
            margin-right: 0.42rem;
            padding: 0.25rem 0.56rem;
            border-radius: 999px;
            background: rgba(29, 78, 216, 0.08);
            color: #0f5f70;
            font-size: 0.77rem;
        }}

        .roadmap {{
            display: grid;
            gap: 0.75rem;
        }}

        .roadmap-step {{
            display: grid;
            grid-template-columns: 88px 1fr;
            gap: 0.9rem;
            padding: 0.96rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.54);
            border: 1px solid rgba(148, 163, 184, 0.14);
        }}

        .roadmap-label {{
            padding: 0.36rem 0.56rem;
            border-radius: 999px;
            text-align: center;
            font-size: 0.76rem;
            font-weight: 800;
            color: var(--secondary);
            background: rgba(20, 184, 166, 0.12);
        }}

        .workflow-step {{
            border-radius: 26px;
            padding: 1.2rem;
            color: #f8fafc;
            height: 100%;
        }}

        .workflow-step h4 {{
            margin: 0.5rem 0 0.56rem;
            font-size: 1.04rem;
        }}

        .workflow-step p {{
            margin: 0;
            color: rgba(248, 250, 252, 0.86);
            font-size: 0.92rem;
            line-height: 1.74;
        }}

        .workflow-1 {{
            background: linear-gradient(135deg, #102a43, var(--secondary));
        }}

        .workflow-2 {{
            background: linear-gradient(135deg, #6f3f14, var(--warning));
        }}

        .workflow-3 {{
            background: linear-gradient(135deg, #2f2b70, var(--accent));
        }}

        .workflow-4 {{
            background: linear-gradient(135deg, #5b1b3b, #db2777);
        }}

        .stButton button {{
            border: none;
            border-radius: 999px;
            padding: 0.68rem 1.12rem;
            color: #ffffff;
            font-weight: 800;
            background: linear-gradient(135deg, var(--secondary), var(--accent));
            box-shadow: 0 14px 28px rgba(29, 78, 216, 0.18);
        }}

        .stSelectbox > div > div,
        .stTextArea textarea,
        .stMultiSelect div[data-baseweb="select"] > div,
        .stDateInput > div > div {{
            border-radius: 18px !important;
        }}

        [data-testid="stDataFrame"] {{
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.14);
        }}

        div[data-baseweb="tab-list"] {{
            gap: 0.55rem;
        }}

        button[role="tab"] {{
            border-radius: 999px !important;
            background: rgba(255, 255, 255, 0.58) !important;
            padding: 0.36rem 0.92rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def chart_style(chart):
    return (
        chart.configure_view(strokeWidth=0)
        .configure_axis(
            labelColor="#4f6478",
            titleColor="#4f6478",
            domain=False,
            tickColor="#cbd5e1",
            gridColor="rgba(148, 163, 184, 0.16)",
        )
        .configure_legend(
            labelColor="#4f6478",
            titleColor="#10263a",
            orient="bottom",
            padding=6,
            cornerRadius=10,
        )
    )


def safe_pct(numerator, denominator):
    if denominator == 0:
        return 0.0
    return numerator / denominator


def section_heading(kicker, title):
    st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="section-title">{title}</h2>', unsafe_allow_html=True)


def metric_card(title, value, delta, tone):
    tone_class = {
        "good": "delta-good",
        "warn": "delta-warn",
        "bad": "delta-bad",
    }.get(tone, "delta-warn")
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <span class="metric-delta {tone_class}">{delta}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_card(title, content, bullets=None):
    bullet_html = ""
    if bullets:
        bullet_html = "<ul>" + "".join(f"<li>{item}</li>" for item in bullets) + "</ul>"
    st.markdown(
        f"""
        <div class="glass-card">
            <h4>{title}</h4>
            <p>{content}</p>
            {bullet_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def signal_card(title, content, bullets=None):
    bullet_html = ""
    if bullets:
        bullet_html = "<ul>" + "".join(f"<li>{item}</li>" for item in bullets) + "</ul>"
    st.markdown(
        f"""
        <div class="signal-card">
            <h4>{title}</h4>
            <p>{content}</p>
            {bullet_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(badge, title, content, bullets=None):
    bullet_html = ""
    if bullets:
        bullet_html = "<ul>" + "".join(f"<li>{item}</li>" for item in bullets) + "</ul>"
    st.markdown(
        f"""
        <div class="feature-card">
            <span class="feature-badge">{badge}</span>
            <h4>{title}</h4>
            <p>{content}</p>
            {bullet_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def manifesto_card(title, content):
    st.markdown(
        f"""
        <div class="manifesto-card">
            <h4>{title}</h4>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def roadmap_card(steps):
    html = ['<div class="timeline-card"><h4>执行路线图</h4><div class="roadmap">']
    for label, text in steps:
        html.append(
            f"""
            <div class="roadmap-step">
                <div class="roadmap-label">{label}</div>
                <div><p style="margin:0;">{text}</p></div>
            </div>
            """
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def review_stream_card(review_row):
    resolved_label = "已跟进" if review_row["is_resolved"] else "待处理"
    st.markdown(
        f"""
        <div class="review-card">
            <div class="review-meta">
                <span>{review_row["review_date"].strftime("%m-%d")} · {review_row["item_name"]}</span>
                <span>{review_row["rating"]} 分 · {resolved_label}</span>
            </div>
            <strong>{review_row["issue_type"]}</strong>
            <p style="margin:0.45rem 0 0.2rem;color:#334b5f;line-height:1.72;">{review_row["review_text"]}</p>
            <span class="tag">关键词：{review_row["keyword"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_reply(issue_type, tone):
    opening = {
        "标准版": "非常抱歉这次体验没有达到您的预期。",
        "诚恳版": "真的很抱歉让您遇到这次不愉快的用餐体验。",
        "补偿引导版": "非常抱歉给您带来了明显的不便，我们理解这会直接影响您的感受。",
    }[tone]
    action = {
        "包装问题": "我们会立即回看该菜品的打包与封口流程，优先处理洒漏和密封不严的问题。",
        "配送问题": "我们会同步复盘该时段的出餐与配送衔接，尽量避免等待过久再次发生。",
        "口味问题": "我们会反馈给出品团队，重新检查这道菜的口味稳定性和出餐标准。",
        "价格问题": "我们会重新评估活动与套餐设计，让价格感知和体验更加匹配。",
        "服务问题": "我们会针对服务环节进行复盘，避免沟通和处理方式再次让您失望。",
    }[issue_type]
    closing = {
        "标准版": "感谢您把真实体验告诉我们，这对我们改进很重要。",
        "诚恳版": "谢谢您直接指出问题，我们会把这次反馈真正落实到改进动作里。",
        "补偿引导版": "如果您愿意，也可以通过平台订单入口继续联系我们，我们会按平台规则协助您处理。",
    }[tone]
    return f"{opening}{action}{closing}"


def filter_data(orders, reviews, marketing, categories, date_range):
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_orders = orders[
        (orders["order_date"] >= start_date)
        & (orders["order_date"] <= end_date)
        & (orders["item_category"].isin(categories))
    ].copy()

    visible_items = filtered_orders["item_name"].unique().tolist()
    filtered_reviews = reviews[
        (reviews["review_date"] >= start_date)
        & (reviews["review_date"] <= end_date)
        & (reviews["item_name"].isin(visible_items))
    ].copy()

    category_items = set(visible_items)

    def campaign_matches(item_list):
        cleaned = {item.strip() for item in item_list}
        return bool(cleaned & category_items)

    filtered_marketing = marketing[
        (marketing["end_date"] >= start_date)
        & (marketing["start_date"] <= end_date)
        & marketing["item_list"].apply(campaign_matches)
    ].copy()

    return filtered_orders, filtered_reviews, filtered_marketing


def compute_metrics(orders, reviews, marketing):
    total_orders = len(orders)
    total_revenue = float(orders["order_amount"].sum()) if not orders.empty else 0.0
    avg_order_amount = float(orders["order_amount"].mean()) if not orders.empty else 0.0
    avg_rating = float(orders["rating"].mean()) if not orders.empty else 0.0
    avg_delivery = float(orders["delivery_minutes"].mean()) if not orders.empty else 0.0
    repeat_rate = float(orders["is_repeat_user"].mean()) if not orders.empty else 0.0

    negative_reviews = reviews[reviews["sentiment"] == "negative"]
    negative_rate = safe_pct(len(negative_reviews), len(reviews))
    packaging_rate = safe_pct(
        len(reviews[reviews["issue_type"] == "包装问题"]), len(reviews)
    )
    resolution_rate = float(reviews["is_resolved"].mean()) if not reviews.empty else 0.0

    issue_counts = (
        reviews[reviews["issue_type"] != "无"]
        .groupby("issue_type")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    top_issue = issue_counts.iloc[0]["issue_type"] if not issue_counts.empty else "暂无风险"

    item_risk = (
        orders.groupby(["item_name", "item_category"])
        .agg(
            order_count=("order_id", "count"),
            revenue=("order_amount", "sum"),
            avg_rating=("rating", "mean"),
            avg_delivery=("delivery_minutes", "mean"),
        )
        .reset_index()
    )

    if not reviews.empty:
        issue_item_counts = (
            reviews[reviews["issue_type"] != "无"]
            .groupby("item_name")
            .size()
            .reset_index(name="issue_count")
        )
        item_risk = item_risk.merge(issue_item_counts, on="item_name", how="left")
    item_risk["issue_count"] = item_risk["issue_count"].fillna(0)
    item_risk["risk_score"] = (
        (5 - item_risk["avg_rating"]) * 18
        + item_risk["issue_count"] * 9
        + (item_risk["avg_delivery"] - 30).clip(lower=0) * 1.2
    )
    worst_item = (
        item_risk.sort_values(["risk_score", "issue_count"], ascending=False).iloc[0]["item_name"]
        if not item_risk.empty
        else "暂无"
    )

    best_campaign = (
        marketing.sort_values("ROI", ascending=False).iloc[0]["campaign_label"]
        if not marketing.empty
        else "暂无活动"
    )

    health_score = round(
        (avg_rating / 5) * 34
        + (1 - negative_rate) * 22
        + (1 - packaging_rate) * 18
        + repeat_rate * 14
        + resolution_rate * 12
        + max(0, 18 - max(avg_delivery - 28, 0) * 1.3)
    )
    health_score = max(0, min(100, health_score))

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_amount": avg_order_amount,
        "avg_rating": avg_rating,
        "avg_delivery": avg_delivery,
        "repeat_rate": repeat_rate,
        "negative_rate": negative_rate,
        "packaging_rate": packaging_rate,
        "resolution_rate": resolution_rate,
        "health_score": health_score,
        "top_issue": top_issue,
        "best_campaign": best_campaign,
        "worst_item": worst_item,
        "issue_counts": issue_counts,
        "item_risk": item_risk,
        "negative_reviews": negative_reviews,
    }


def render_brand_header(metrics, mode_key, categories, date_range):
    mode = MODE_CONFIG[mode_key]
    category_text = "、".join(categories[:3])
    if len(categories) > 3:
        category_text += " 等"

    st.markdown(
        f"""
        <div class="brand-header">
            <div class="brand-lockup">
                <div class="eyebrow">{mode["eyebrow"]}</div>
                <div class="brand-row">
                    <div class="brand-mark">MM</div>
                    <div>
                        <div class="brand-name">MealMind AI</div>
                        <div class="brand-subtitle">Smart Operating System for Modern Food Brands</div>
                    </div>
                </div>
                <h1>{mode["headline"]}</h1>
                <p>{mode["description"]}</p>
                <div class="brand-pill-row">
                    <span class="brand-pill"><strong>品牌模式</strong>：{mode["label"]}</span>
                    <span class="brand-pill"><strong>经营健康度</strong>：{metrics["health_score"]}/100</span>
                    <span class="brand-pill"><strong>当前风险</strong>：{metrics["top_issue"]}</span>
                    <span class="brand-pill"><strong>重点菜品</strong>：{metrics["worst_item"]}</span>
                </div>
            </div>
            <div class="brand-radar">
                <div class="section-kicker" style="margin-top:0;">Operating Snapshot</div>
                <h3>当前经营概览</h3>
                <p>你可以按时间、品类和经营主题切换视角，快速查看不同经营切片下的风险、机会和优先动作。</p>
                <div class="score-wrap">
                    <div class="score-ring">
                        <div class="score-inner">{metrics["health_score"]}</div>
                    </div>
                    <div class="score-notes">
                        <p><strong>观察区间：</strong>{pd.to_datetime(date_range[0]).strftime("%m.%d")} - {pd.to_datetime(date_range[1]).strftime("%m.%d")}</p>
                        <p><strong>聚焦品类：</strong>{category_text}</p>
                        <p><strong>最优活动：</strong>{metrics["best_campaign"]}</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_manifesto(metrics):
    section_heading("Why MealMind", "一套围绕真实经营场景设计的 AI 产品")
    st.markdown(
        f"""
        <div class="notice-card">
            MealMind AI 面向连锁餐饮和成长型门店团队，提供一套覆盖风险识别、口碑恢复、增长判断与执行协同的智能经营系统。
            它把原本散落在平台后台、评论区和营销报表里的信息，整理成一个更统一、更可执行的产品体验。
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        manifesto_card(
            "从分散数据到统一判断",
            "订单、评价、营销和客服信息会在这里汇总成同一套经营视图，商家不需要在多个后台之间来回切换，就能快速看到真正影响结果的关键问题。"
        )
    with right:
        manifesto_card(
            "从问题发现到动作落地",
            f"当前最需要关注的是 {metrics['top_issue']}。MealMind AI 不只指出问题，还会进一步连接商品治理、用户安抚与增长决策，让判断真正变成经营动作。"
        )

    st.markdown(
        """
        <div class="trust-strip">
            <div class="trust-chip">经营驾驶舱</div>
            <div class="trust-chip">口碑修复引擎</div>
            <div class="trust-chip">增长实验台</div>
            <div class="trust-chip">客服协同工作流</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard(orders, reviews, marketing, metrics):
    section_heading("Product Overview", "产品首页")

    features = st.columns(3)
    with features[0]:
        feature_card(
            "Product",
            "经营驾驶舱",
            "把订单、评分、配送和复购等核心指标整合进一个首页视图，让商家先看到真正影响经营结果的关键信号。",
            ["一屏看健康度与风险", "优先级更清晰", "适合门店与品牌团队共用"],
        )
    with features[1]:
        feature_card(
            "Recovery",
            "口碑修复引擎",
            "围绕差评、包装、履约和客服动作建立统一恢复链路，帮助商家更快压降负面体验并恢复用户信心。",
            ["差评标签化归因", "客服话术联动经营动作", "适合高频问题持续治理"],
        )
    with features[2]:
        feature_card(
            "Growth",
            "增长实验台",
            "把投放、套餐、新客与复购策略放进同一套实验框架，帮助团队在稳定体验之后有节奏地放大增长。",
            ["新客与老客分层", "ROI 与评分联动看", "更适合持续复盘"],
        )

    row_1 = st.columns(4)
    with row_1[0]:
        metric_card("订单量", f'{metrics["total_orders"]}', "当前样本内表现", "warn")
    with row_1[1]:
        metric_card("营业额", f'¥{metrics["total_revenue"]:,.0f}', "当前样本总收入", "good")
    with row_1[2]:
        metric_card("平均评分", f'{metrics["avg_rating"]:.2f}', "口碑质量核心信号", "bad")
    with row_1[3]:
        metric_card("平均配送时长", f'{metrics["avg_delivery"]:.1f} 分钟', "履约体验关键项", "warn")

    row_2 = st.columns(4)
    with row_2[0]:
        metric_card("客单价", f'¥{metrics["avg_order_amount"]:.1f}', "订单价值表现", "good")
    with row_2[1]:
        metric_card("差评率", f'{metrics["negative_rate"]:.1%}', "负向反馈占比", "bad")
    with row_2[2]:
        metric_card("包装问题占比", f'{metrics["packaging_rate"]:.1%}', "主要风险来源", "bad")
    with row_2[3]:
        metric_card("复购用户占比", f'{metrics["repeat_rate"]:.1%}', "留存质量信号", "warn")

    st.markdown(
        f"""
        <div class="notice-card">
            当前最值得优先处理的不是单纯增加投放，而是先解决 <strong>{metrics["top_issue"]}</strong> 对 <strong>{metrics["worst_item"]}</strong> 带来的体验损耗。
            先稳住评分和履约体验，再放大增长，通常会得到更健康的经营结果。
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("Live Preview", "产品实时视图")
    tabs = st.tabs(["经营雷达", "菜单风险", "增长模拟"])

    with tabs[0]:
        daily_orders = (
            orders.groupby("order_date")
            .size()
            .reset_index(name="order_count")
            .sort_values("order_date")
        )
        issue_counts = metrics["issue_counts"]

        trend_chart = chart_style(
            alt.Chart(daily_orders)
            .mark_area(
                line={"color": "#1d4ed8", "strokeWidth": 3},
                color=alt.Gradient(
                    gradient="linear",
                    stops=[
                        alt.GradientStop(color="rgba(29,78,216,0.42)", offset=0),
                        alt.GradientStop(color="rgba(29,78,216,0.02)", offset=1),
                    ],
                    x1=1,
                    x2=1,
                    y1=1,
                    y2=0,
                ),
            )
            .encode(
                x=alt.X("order_date:T", title="日期"),
                y=alt.Y("order_count:Q", title="订单量"),
                tooltip=["order_date:T", "order_count:Q"],
            )
            .properties(height=320)
        )

        issue_chart = chart_style(
            alt.Chart(issue_counts)
            .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
            .encode(
                x=alt.X("count:Q", title="评论数量"),
                y=alt.Y("issue_type:N", sort="-x", title="问题类型"),
                color=alt.Color(
                    "issue_type:N",
                    scale=alt.Scale(range=["#f97316", "#fb7185", "#0ea5e9", "#8b5cf6"]),
                    legend=None,
                ),
                tooltip=["issue_type:N", "count:Q"],
            )
            .properties(height=320)
        )

        left, right = st.columns(2)
        with left:
            st.altair_chart(trend_chart, use_container_width=True)
        with right:
            st.altair_chart(issue_chart, use_container_width=True)

        insights = st.columns(3)
        with insights[0]:
            signal_card(
                "为什么首页先看这些",
                "产品首页优先展示经营健康、主要风险、关键品类和增长空间，因为这些信息最能帮助商家快速判断下一步动作。",
                ["适合快速扫读", "适合管理者判断优先级", "适合作为每日经营入口"],
            )
        with insights[1]:
            signal_card(
                "产品如何帮助判断",
                "当订单、评分和风险问题同时变化时，系统会优先提醒体验问题，而不是只给出更多投放建议。",
                ["先压包装问题", "再修配送感知", "最后回到投放放大"],
            )
        with insights[2]:
            signal_card(
                "适合谁来用",
                "既适合门店负责人快速掌握经营状态，也适合品牌团队做更高层级的口碑和增长判断。",
                ["门店日常复盘", "品牌区域巡检", "运营策略评估"],
            )

    with tabs[1]:
        item_risk = metrics["item_risk"]
        hourly_mix = (
            orders.groupby("hour")
            .size()
            .reset_index(name="order_count")
            .sort_values("hour")
        )

        risk_chart = chart_style(
            alt.Chart(item_risk)
            .mark_circle(opacity=0.85, stroke="white", strokeWidth=1.4)
            .encode(
                x=alt.X("avg_rating:Q", title="平均评分"),
                y=alt.Y("issue_count:Q", title="问题评论数"),
                size=alt.Size("revenue:Q", title="营业额"),
                color=alt.Color(
                    "item_category:N",
                    scale=alt.Scale(range=["#0f766e", "#1d4ed8", "#d97706", "#e11d48"]),
                    title="品类",
                ),
                tooltip=[
                    "item_name:N",
                    "item_category:N",
                    "avg_rating:Q",
                    "issue_count:Q",
                    "revenue:Q",
                ],
            )
            .properties(height=340)
        )

        hourly_chart = chart_style(
            alt.Chart(hourly_mix)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, color="#0f766e")
            .encode(
                x=alt.X("hour:O", title="下单时段"),
                y=alt.Y("order_count:Q", title="订单量"),
                tooltip=["hour:O", "order_count:Q"],
            )
            .properties(height=340)
        )

        left, right = st.columns(2)
        with left:
            st.altair_chart(risk_chart, use_container_width=True)
        with right:
            st.altair_chart(hourly_chart, use_container_width=True)

        st.dataframe(
            item_risk.sort_values("risk_score", ascending=False)[
                [
                    "item_name",
                    "item_category",
                    "order_count",
                    "revenue",
                    "avg_rating",
                    "avg_delivery",
                    "issue_count",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    with tabs[2]:
        improvement_packaging = st.slider("包装问题改善比例", 0, 60, 25, 5)
        improvement_delivery = st.slider("平均配送缩短分钟数", 0, 15, 6, 1)
        recovery_repeat = st.slider("复购率提升百分点", 0, 30, 8, 1)

        projected_packaging = metrics["packaging_rate"] * (1 - improvement_packaging / 100)
        projected_delivery = max(metrics["avg_delivery"] - improvement_delivery, 18)
        projected_repeat = min(metrics["repeat_rate"] + recovery_repeat / 100, 0.95)
        projected_score = round(
            (metrics["avg_rating"] / 5) * 34
            + (1 - metrics["negative_rate"]) * 22
            + (1 - projected_packaging) * 18
            + projected_repeat * 14
            + metrics["resolution_rate"] * 12
            + max(0, 18 - max(projected_delivery - 28, 0) * 1.3)
        )
        projected_score = max(0, min(100, projected_score))

        sim = st.columns(3)
        with sim[0]:
            metric_card("当前健康度", f'{metrics["health_score"]}', "现在的品牌盘面", "warn")
        with sim[1]:
            metric_card("模拟后健康度", f"{projected_score}", "按当前滑块估算", "good")
        with sim[2]:
            metric_card("可争取提升", f"+{projected_score - metrics['health_score']}", "这是增长弹性", "good")

        roadmap_card(
            [
                ("24h", "替换高风险汤类包装并安排抽检，先压住最明显的洒漏问题。"),
                ("7d", "更新商品页文案与卖点，突出防洒、分装和履约说明。"),
                ("14d", "对老客做定向安抚与复购券回流，观察评分修复和复购回升。"),
                ("30d", "把修复后的稳定菜品重新纳入增长投放，扩大更健康的订单结构。"),
            ]
        )

    st.markdown(
        """
        <div class="cta-banner">
            <h3>把经营判断从“看懂数据”，升级成“持续做出更好的动作”。</h3>
            <p>
                MealMind AI 适合用作餐饮品牌的经营首页、区域巡检入口和门店复盘工作台。
                在同一套界面里，团队可以同时处理评分、差评、履约、营销和客服协同问题，让经营动作更有节奏。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_report(question_type, marketing, metrics):
    if question_type == "为什么我这周订单下降了？":
        return {
            "headline": "订单下降更像是体验端损伤带来的转化回落，而不是自然流量突然消失。",
            "impact": "高优先级",
            "evidence": [
                f"当前平均评分为 {metrics['avg_rating']:.2f}，不足以稳定支撑复购和转化。",
                f"当前最大风险是 {metrics['top_issue']}，说明问题具有系统性，而非偶发。",
                f"{metrics['worst_item']} 是当前最值得优先治理的高风险菜品。",
            ],
            "actions": [
                "先修包装和履约体验，避免继续放大差评。",
                "在商品页增加包装升级与防洒说明，降低用户心理落差。",
                "用老客回流券去验证体验修复后复购是否回升。",
            ],
        }
    if question_type == "最近为什么差评变多了？":
        return {
            "headline": f"差评上升的核心原因是 {metrics['top_issue']} 正在从单点问题变成持续风险。",
            "impact": "风险升温",
            "evidence": [
                "问题关键词持续重复，说明用户感知已形成模式。",
                f"当前差评率为 {metrics['negative_rate']:.1%}，继续放任会影响平台转化。",
                "客服闭环和经营动作还没有真正打通。",
            ],
            "actions": [
                "把差评问题拆到商品、履约、客服三个负责人。",
                "优先排查汤类和高峰时段的风险链路。",
                "让问题标签自动进入每周经营复盘。",
            ],
        }
    if question_type == "这次营销活动为什么效果不好？":
        weakest = (
            marketing.sort_values("ROI", ascending=True).iloc[0]["campaign_type"]
            if not marketing.empty
            else "当前活动"
        )
        return {
            "headline": f"{CAMPAIGN_LABELS.get(weakest, weakest)} 表现偏弱，问题不只是优惠力度，而是投放策略和体验状态没有对齐。",
            "impact": "投放效率偏低",
            "evidence": [
                "部分活动实际增长低于预期，说明优惠没有充分转成有效订单。",
                "存在把风险菜品直接推给用户的情况，会放大获客成本。",
                "新客和老客策略仍然不够分层。",
            ],
            "actions": [
                "让稳定菜品承担引流任务，而不是让高风险菜品背流量目标。",
                "把新客券、复购券和套餐活动拆分成不同增长动作。",
                "体验修复前，暂停放大高风险菜品投放。",
            ],
        }
    return {
        "headline": "最该优先优化的不是销量最低的菜，而是差评密度高、会拖累复购的关键菜品。",
        "impact": "立即优化",
        "evidence": [
            f"{metrics['worst_item']} 当前最值得优先治理。",
            "汤类菜品的问题更集中，说明专项治理更容易快速见效。",
            "在修复前继续重投，只会加速负面体验传播。",
        ],
        "actions": [
            "专项升级高风险菜品包装和分装结构。",
            "强化商品页文案，把包装升级变成用户可感知的卖点。",
            "修复完成前，控制高风险菜品的大额促销节奏。",
        ],
    }


def render_diagnosis(orders, marketing, metrics):
    section_heading("AI Diagnosis", "经营诊断")

    question_type = st.selectbox(
        "选择一个最想展示给别人看的经营问题",
        [
            "为什么我这周订单下降了？",
            "最近为什么差评变多了？",
            "这次营销活动为什么效果不好？",
            "哪些菜品最需要优先优化？",
        ],
    )
    report = build_report(question_type, marketing, metrics)

    top = st.columns([2, 1, 1])
    with top[0]:
        signal_card("一句话判断", report["headline"])
    with top[1]:
        metric_card(
            "问题等级",
            report["impact"],
            "需要经营动作闭环",
            "bad" if report["impact"] in {"高优先级", "立即优化"} else "warn",
        )
    with top[2]:
        metric_card(
            "观察窗口",
            f"{orders['order_date'].min():%m.%d}-{orders['order_date'].max():%m.%d}",
            "当前筛选样本",
            "good",
        )

    tabs = st.tabs(["证据板", "行动板", "汇报口径"])

    with tabs[0]:
        cols = st.columns(2)
        with cols[0]:
            signal_card(
                "关键证据",
                "系统会把分散的数据线索整理成可以直接用于判断和汇报的经营证据。",
                report["evidence"],
            )
        with cols[1]:
            glass_card(
                "系统补充判断",
                f"如果评分、包装和配送时长同时出现波动，优先级就不应放在追加营销预算，而应先放在体验修复。当前最大问题是 {metrics['top_issue']}，它已经影响到整体经营质量。",
            )

    with tabs[1]:
        roadmap_card(
            [
                ("T+1", report["actions"][0]),
                ("T+7", report["actions"][1]),
                ("T+30", report["actions"][2]),
            ]
        )

    with tabs[2]:
        glass_card(
            "汇报时可以这样讲",
            f"MealMind AI 识别到的不是单个异常点，而是由 {metrics['top_issue']} 引发的连续经营影响：它会同时作用于评分、复购和营销效率。下一步更优策略是先修复体验，把底盘稳住，再做增长放量。",
        )


def render_review_analysis(reviews, metrics):
    section_heading("Review Intelligence", "评价洞察")

    stats = st.columns(4)
    with stats[0]:
        metric_card("负面评论占比", f'{metrics["negative_rate"]:.1%}', "口碑压力值", "bad")
    with stats[1]:
        metric_card("已解决评论占比", f'{metrics["resolution_rate"]:.1%}', "闭环效率", "warn")
    with stats[2]:
        metric_card("最高频问题", metrics["top_issue"], "当前主要矛盾", "bad")
    with stats[3]:
        metric_card("高风险菜品", metrics["worst_item"], "优先处理对象", "warn")

    sentiment_counts = (
        reviews.groupby("sentiment")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    issue_counts = metrics["issue_counts"]
    issue_items = (
        reviews[reviews["issue_type"] != "无"]
        .groupby(["item_name", "issue_type"])
        .size()
        .reset_index(name="issue_count")
        .sort_values("issue_count", ascending=False)
    )

    donut = chart_style(
        alt.Chart(sentiment_counts)
        .mark_arc(innerRadius=58, outerRadius=98)
        .encode(
            theta="count:Q",
            color=alt.Color(
                "sentiment:N",
                scale=alt.Scale(
                    domain=["positive", "neutral", "negative"],
                    range=["#0f766e", "#f59e0b", "#e11d48"],
                ),
                title="情绪分布",
            ),
            tooltip=["sentiment:N", "count:Q"],
        )
        .properties(height=310)
    )

    issue_chart = chart_style(
        alt.Chart(issue_counts)
        .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
        .encode(
            x=alt.X("count:Q", title="评论数量"),
            y=alt.Y("issue_type:N", sort="-x", title="问题类型"),
            color=alt.value("#fb7185"),
            tooltip=["issue_type:N", "count:Q"],
        )
        .properties(height=310)
    )

    left, right = st.columns(2)
    with left:
        st.altair_chart(donut, use_container_width=True)
    with right:
        st.altair_chart(issue_chart, use_container_width=True)

    tabs = st.tabs(["问题菜品", "评论流", "恢复建议"])

    with tabs[0]:
        pivot_table = issue_items.pivot_table(
            index="item_name", columns="issue_type", values="issue_count", fill_value=0
        ).reset_index()
        st.dataframe(pivot_table, use_container_width=True, hide_index=True)

    with tabs[1]:
        feed_col, summary_col = st.columns([1.2, 0.9])
        with feed_col:
            for _, row in metrics["negative_reviews"].head(6).iterrows():
                review_stream_card(row)
        with summary_col:
            signal_card(
                "系统总结",
                "差评真正值得关注的不是情绪本身，而是问题是否在重复。只要关键词持续重复，它就已经不是偶发事故，而是经营流程里某个环节需要被系统性修复。",
                ["优先修复重复率最高的问题", "差评标签回流商品优化", "客服安抚要和经营动作同步"],
            )

    with tabs[2]:
        roadmap_card(
            [
                ("客服", "对包装和配送投诉建立统一安抚口径，减少二次负面体验。"),
                ("商品", "高风险菜品优先升级包装和商品描述。"),
                ("运营", "让差评问题进入每周经营复盘，持续跟踪评分和复购修复。"),
            ]
        )


def render_marketing(marketing, metrics):
    section_heading("Growth Story", "营销分析")

    avg_roi = float(marketing["ROI"].mean()) if not marketing.empty else 0.0
    best = marketing.sort_values("ROI", ascending=False).iloc[0] if not marketing.empty else None
    weakest = marketing.sort_values("ROI", ascending=True).iloc[0] if not marketing.empty else None

    top = st.columns(3)
    with top[0]:
        metric_card("平均 ROI", f"{avg_roi:.2f}", "当前活动组合表现", "warn")
    with top[1]:
        metric_card(
            "最佳活动",
            best["campaign_label"] if best is not None else "暂无",
            f'ROI {best["ROI"]:.1f}' if best is not None else "等待数据",
            "good",
        )
    with top[2]:
        metric_card(
            "最弱活动",
            weakest["campaign_label"] if weakest is not None else "暂无",
            f'ROI {weakest["ROI"]:.1f}' if weakest is not None else "等待数据",
            "bad",
        )

    roi_chart = chart_style(
        alt.Chart(marketing)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("campaign_label:N", sort="-y", title="活动类型"),
            y=alt.Y("ROI:Q", title="ROI"),
            color=alt.condition(
                alt.datum.ROI >= 1.2, alt.value("#0f766e"), alt.value("#f59e0b")
            ),
            tooltip=["campaign_label:N", "target_user_group:N", "ROI:Q"],
        )
        .properties(height=320)
    )

    scatter = chart_style(
        alt.Chart(marketing)
        .mark_circle(size=220, opacity=0.86, stroke="white", strokeWidth=1.2)
        .encode(
            x=alt.X("expected_lift:Q", title="预期增长 (%)"),
            y=alt.Y("actual_lift:Q", title="实际增长 (%)"),
            color=alt.Color(
                "target_user_group:N",
                scale=alt.Scale(range=["#1d4ed8", "#0f766e", "#f97316"]),
                title="目标人群",
            ),
            tooltip=[
                "campaign_label:N",
                "items_involved:N",
                "expected_lift:Q",
                "actual_lift:Q",
                "ROI:Q",
            ],
        )
        .properties(height=320)
    )

    left, right = st.columns(2)
    with left:
        st.altair_chart(roi_chart, use_container_width=True)
    with right:
        st.altair_chart(scatter, use_container_width=True)

    cols = st.columns(3)
    with cols[0]:
        signal_card(
                "该保留什么",
                "新客券和套餐组合更适合承担当前增长入口，因为它们更容易被用户感知为清晰的价值承诺。",
                ["拉新更稳定", "价值更好理解"],
            )
    with cols[1]:
        signal_card(
            "该暂停什么",
            f"在 {metrics['top_issue']} 修复前，不建议继续放大高风险菜品促销，否则会稀释所有投放效率。",
            ["避免放大差评", "减少无效获客成本"],
        )
    with cols[2]:
        signal_card(
            "该升级什么",
            "把营销从简单优惠升级成品牌策略：体验修复后，再用稳定菜品承担增长任务。",
            ["新客、老客、套餐拆分运营", "ROI 和评分一起看", "引流菜品优先选稳定品类"],
        )

    st.dataframe(marketing, use_container_width=True, hide_index=True)


def render_customer_service(metrics):
    section_heading("Care Studio", "把客服能力也包装成品牌产品的一部分")

    left, right = st.columns([1, 1.45])
    with left:
        st.text_area(
            "用户评价样例",
            value="汤全洒了，包装太差了，等了很久才送到。",
            height=180,
        )
        issue_type = st.selectbox(
            "问题类型",
            ["包装问题", "配送问题", "口味问题", "价格问题", "服务问题"],
        )
        tone_focus = st.selectbox(
            "建议优先语气",
            ["诚恳版", "标准版", "补偿引导版"],
        )
        glass_card(
            "客服不该独立存在",
            f"这块能力不只是生成一句回复，而是把 {metrics['top_issue']} 这类经营问题同步回品牌修复动作里，让客服成为口碑恢复系统的一部分。",
        )

    with right:
        reply_cols = st.columns(3)
        tones = ["标准版", "诚恳版", "补偿引导版"]
        for col, tone in zip(reply_cols, tones):
            with col:
                badge = "推荐" if tone == tone_focus else "可选"
                reply = build_reply(issue_type, tone)
                st.markdown(
                    f"""
                    <div class="reply-card">
                        <h4>{tone} · {badge}</h4>
                        <p>{reply}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        summary = st.columns(2)
        with summary[0]:
            signal_card(
                "推荐回复结构",
                "先共情，再说明已采取的动作，最后给出平台内继续处理路径，这样更像一个成熟品牌的回应方式。",
                ["不要甩锅给骑手", "不要平台外承诺补偿", "严重投诉引导回平台流程"],
            )
        with summary[1]:
            signal_card(
                "为什么这版更完整",
                "它把不同语气版本并排展示，还让客服话术和经营风险直接联动，不再只是简单文本生成。",
                ["更像产品能力卡片", "更适合汇报展示", "后续更容易接入真实 LLM"],
            )


def render_workflow():
    section_heading("System Narrative", "Agent 协作流程")

    steps = st.columns(4)
    step_data = [
        ("01", "问题识别", "先判断商家提问属于订单、口碑、营销还是客服恢复。", "workflow-1"),
        ("02", "证据分析", "订单、评价和营销数据分别给出趋势、原因和经营信号。", "workflow-2"),
        ("03", "策略编排", "把问题转换成商品优化、分层投放和客服回应三类动作。", "workflow-3"),
        ("04", "报告输出", "最终沉淀成一份可展示、可执行、可复盘的经营诊断报告。", "workflow-4"),
    ]
    for column, (idx, title, body, style_class) in zip(steps, step_data):
        with column:
            st.markdown(
                f"""
                <div class="workflow-step {style_class}">
                    <div class="eyebrow">{idx}</div>
                    <h4>{title}</h4>
                    <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    lower = st.columns([1, 1])
    with lower[0]:
        glass_card(
            "系统说明",
            "这一页展示的是 MealMind AI 如何把订单、评价、营销和客服信息串成一套完整的决策流程，让建议不仅可看，还能落到执行。",
            ["适合作品集讲故事", "适合解释产品逻辑", "适合后续接入多 Agent"],
        )
    with lower[1]:
        roadmap_card(
            [
                ("Data", "订单、评价、营销数据进入统一的数据视图。"),
                ("Logic", "规则或模型判断风险、优先级和增长机会。"),
                ("Action", "为商家生成商品、营销、客服三类动作。"),
                ("Loop", "持续观察评分、差评率、复购率和 ROI 的变化。"),
            ]
        )

    agent_table = pd.DataFrame(
        {
            "Agent": ["数据分析 Agent", "评价洞察 Agent", "营销策略 Agent", "客服话术 Agent"],
            "输入": [
                "订单、评分、配送时长、复购数据",
                "评价文本、关键词、问题标签、处理状态",
                "活动 ROI、目标人群、菜品表现",
                "用户反馈、问题类型、商家语气偏好",
            ],
            "输出": [
                "趋势异常、核心风险、指标波动说明",
                "高频问题、问题菜品、典型用户情绪",
                "投放建议、活动分层、风险提示",
                "标准回复、诚恳回复、补偿引导回复",
            ],
        }
    )
    st.dataframe(agent_table, use_container_width=True, hide_index=True)


orders_df, reviews_df, marketing_df = load_data()

all_categories = sorted(orders_df["item_category"].unique().tolist())
min_date = orders_df["order_date"].min().date()
max_date = orders_df["order_date"].max().date()

st.sidebar.markdown("## MealMind AI")
st.sidebar.markdown("面向餐饮品牌的智能经营决策系统。")

mode_key = st.sidebar.selectbox("品牌模式", list(MODE_CONFIG.keys()))
mode = MODE_CONFIG[mode_key]
inject_styles(mode["accent"], mode["secondary"], mode["warning"])

page = st.sidebar.radio(
    "浏览模块",
    ["产品首页", "AI 经营诊断", "差评归因分析", "营销活动分析", "客服回复生成", "Agent 工作流"],
)
categories = st.sidebar.multiselect("聚焦品类", options=all_categories, default=all_categories)
date_range = st.sidebar.date_input(
    "观察周期",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if not categories:
    st.warning("请至少选择一个品类。")
    st.stop()

if len(date_range) != 2:
    st.warning("请选择完整的起止日期。")
    st.stop()

filtered_orders, filtered_reviews, filtered_marketing = filter_data(
    orders_df,
    reviews_df,
    marketing_df,
    categories,
    date_range,
)

if filtered_orders.empty or filtered_reviews.empty:
    st.warning("当前筛选条件下没有足够数据，试着放宽品类或日期范围。")
    st.stop()

metrics = compute_metrics(filtered_orders, filtered_reviews, filtered_marketing)

st.sidebar.markdown(
    f"""
    <div class="glass-card" style="background:rgba(255,255,255,0.09);border:1px solid rgba(255,255,255,0.10);box-shadow:none;">
        <h4 style="color:#ffffff;margin-bottom:0.45rem;">品牌健康度</h4>
        <p style="font-size:2rem;font-weight:800;color:#ffffff;line-height:1;margin:0 0 0.45rem;">{metrics["health_score"]}</p>
        <p style="color:rgba(255,255,255,0.76);margin:0;">先解决 {metrics["top_issue"]}，再放大品牌增长。</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("### 本轮叙事焦点")
st.sidebar.markdown(f"- 主要风险：{metrics['top_issue']}")
st.sidebar.markdown(f"- 关键菜品：{metrics['worst_item']}")
st.sidebar.markdown(f"- 最佳活动：{metrics['best_campaign']}")
st.sidebar.markdown(f"- 当前模式：{mode['label']}")

render_brand_header(metrics, mode_key, categories, date_range)
render_manifesto(metrics)

if page == "产品首页":
    render_dashboard(filtered_orders, filtered_reviews, filtered_marketing, metrics)
elif page == "AI 经营诊断":
    render_diagnosis(filtered_orders, filtered_marketing, metrics)
elif page == "差评归因分析":
    render_review_analysis(filtered_reviews, metrics)
elif page == "营销活动分析":
    render_marketing(filtered_marketing, metrics)
elif page == "客服回复生成":
    render_customer_service(metrics)
else:
    render_workflow()

