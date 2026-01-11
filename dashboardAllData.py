import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_abiyyu(abiyyu):
    daily_orders_abiyyu = abiyyu.resample(rule='D', on='order_date').agg({
        "order_id": "nunique",
        "total_price": "sum"
    })
    daily_orders_abiyyu = daily_orders_abiyyu.reset_index()
    daily_orders_abiyyu.rename(columns={
        "order_id": "order_count",
        "total_price": "revenue"
    }, inplace=True)
    
    return daily_orders_abiyyu

def create_daily_orders_abiyyu(abiyyu):
    daily_orders_abiyyu = abiyyu.resample(rule='D', on='order_date').agg({
        "order_id": "nunique",
        "total_price": "sum"
    })
    daily_orders_abiyyu = daily_orders_abiyyu.reset_index()
    daily_orders_abiyyu.rename(columns={
        "order_id": "order_count",
        "total_price": "revenue"
    }, inplace=True)
    
    return daily_orders_abiyyu

def create_sum_order_items_abiyyu(abiyyu):
    sum_order_items_abiyyu = abiyyu.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_abiyyu

def create_bygender_abiyyu(abiyyu):
    bygender_abiyyu = abiyyu.groupby("gender").customer_id.nunique().reset_index()
    bygender_abiyyu.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bygender_abiyyu

def create_byage_abiyyu(abiyyu):
    byage_abiyyu = abiyyu.groupby(by="age_group").customer_id.nunique().reset_index()
    byage_abiyyu.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    byage_abiyyu['age_group'] = pd.Categorical(byage_abiyyu['age_group'], ["Youth", "Adults", "Seniors"])
    
    return byage_abiyyu

def create_bystate_abiyyu(abiyyu):
    bystate_abiyyu = abiyyu.groupby(by="state").customer_id.nunique().reset_index()
    bystate_abiyyu.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_abiyyu

def create_rfm_abiyyu(abiyyu):
    rfm_abiyyu = abiyyu.groupby(by="customer_id", as_index=False).agg({
        "order_date": "max", #mengambil tanggal order terakhir
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_abiyyu.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_abiyyu["max_order_timestamp"] = rfm_abiyyu["max_order_timestamp"].dt.date
    recent_date = abiyyu["order_date"].dt.date.max()
    rfm_abiyyu["recency"] = rfm_abiyyu["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_abiyyu.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_abiyyu

all_abiyyu = pd.read_csv("all_data.csv")

datetime_columns = ["order_date", "delivery_date"]
all_abiyyu.sort_values(by="order_date", inplace=True)
all_abiyyu.reset_index(inplace=True)
 
for column in datetime_columns:
    all_abiyyu[column] = pd.to_datetime(all_abiyyu[column])

min_date = all_abiyyu["order_date"].min()
max_date = all_abiyyu["order_date"].max()
 
with st.sidebar:
    
    st.image("https://raw.githubusercontent.com/mhvvn/dashboard_streamlit/refs/heads/main/img/tshirt.png", width=80)
    
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_abiyyu = all_abiyyu[(all_abiyyu["order_date"] >= str(start_date)) & 
                (all_abiyyu["order_date"] <= str(end_date))]

daily_orders_abiyyu = create_daily_orders_abiyyu(main_abiyyu)
sum_order_items_abiyyu = create_sum_order_items_abiyyu(main_abiyyu)
bygender_abiyyu = create_bygender_abiyyu(main_abiyyu)
byage_abiyyu = create_byage_abiyyu(main_abiyyu)
bystate_abiyyu = create_bystate_abiyyu(main_abiyyu)
rfm_abiyyu = create_rfm_abiyyu(main_abiyyu)

st.header('My Collection Dashboard :sparkles:')

st.subheader("Daily Orders")

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_abiyyu["order_count"].sum()
    st.metric("Total orders", total_orders)

with col2:
    total_revenue = format_currency(
        daily_orders_abiyyu["revenue"].sum(),
        "AUD",
        locale="es_CO"
    )
    st.metric("Total Revenue", total_revenue)

fig = px.line(
    daily_orders_abiyyu,
    x="order_date",
    y="order_count",
    markers=True,
    title="Daily Order Trend"
)

fig.update_traces(
    line=dict(width=2, color="#90CAF9"),
    marker=dict(size=6)
)

fig.update_layout(
    xaxis_title="Order Date",
    yaxis_title="Order Count",
    template="plotly_white",
    height=450,
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=16
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Best & Worst Performing Product")
 
best_abiyyu = (
    sum_order_items_abiyyu
    .sort_values(by="quantity_x", ascending=False)
    .head(5)
)

worst_abiyyu = (
    sum_order_items_abiyyu
    .sort_values(by="quantity_x", ascending=True)
    .head(5)
)

col1, col2 = st.columns(2)

with col1:
    fig_best = px.bar(
        best_abiyyu,
        x="quantity_x",
        y="product_name",
        orientation="h",
        title="Best Performing Product",
        color="product_name",
        labels={
            "quantity_x": "quantity_x",
            "product_name": "product_name"
        },
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(fig_best, use_container_width=True)

with col2:
    fig_worst = px.bar(
        worst_abiyyu,
        x="quantity_x",
        y="product_name",
        orientation="h",
        title="Worst Performing Product",
        color="product_name",
        labels={
            "quantity_x": "quantity_x",
            "product_name": "product_name"
        },
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(fig_worst, use_container_width=True)

st.subheader("Customer Demographics")

fig_gender = px.bar(
    bygender_abiyyu.sort_values(by="customer_count", ascending=False),
    x="gender",
    y="customer_count",
    color="gender",
    title="Number of Customer by Gender",
    labels={
        "gender": "gender",
        "customer_count": "customer_count"
    },
    height=450,
    template="plotly_dark"
)

st.plotly_chart(fig_gender, use_container_width=True)

fig_age = px.bar(
    byage_abiyyu.sort_values(by="customer_count", ascending=False),
    x="age_group",
    y="customer_count",
    color="age_group",
    title="Number of Customer by Age Group",
    labels={
        "age_group": "age_group",
        "customer_count": "customer_count"
    },
    height=450,
    template="plotly_dark"
)

st.plotly_chart(fig_age, use_container_width=True)

fig_state = px.bar(
    bystate_abiyyu.sort_values(by="customer_count", ascending=False),
    x="customer_count",
    y="state",
    orientation="h",
    color="state",
    title="Number of Customer by State",
    labels={
        "customer_count": "customer_count",
        "state": "state"
    },
    height=550,
    template="plotly_dark"
)

st.plotly_chart(fig_state, use_container_width=True)

st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

avg_recency = round(rfm_abiyyu["recency"].mean(), 1)
avg_frequency = round(rfm_abiyyu["frequency"].mean(), 2)
avg_monetary = f"AUD {rfm_abiyyu['monetary'].mean():,.2f}"

with col1:
    st.metric("Average Recency (days)", avg_recency)

with col2:
    st.metric("Average Frequency", avg_frequency)

with col3:
    st.metric("Average Monetary", avg_monetary)

st.markdown("---")

top_recency = rfm_abiyyu.sort_values("recency", ascending=True).head(5)
top_frequency = rfm_abiyyu.sort_values("frequency", ascending=False).head(5)
top_monetary = rfm_abiyyu.sort_values("monetary", ascending=False).head(5)

fig_recency = px.bar(
    top_recency,
    x="customer_id",
    y="recency",
    title="Top Customers by Recency",
    template="plotly_dark"
)

fig_frequency = px.bar(
    top_frequency,
    x="customer_id",
    y="frequency",
    title="Top Customers by Frequency",
    template="plotly_dark"
)

fig_monetary = px.bar(
    top_monetary,
    x="customer_id",
    y="monetary",
    title="Top Customers by Monetary",
    template="plotly_dark"
)

c1, c2, c3 = st.columns(3)

with c1:
    st.plotly_chart(fig_recency, use_container_width=True)

with c2:
    st.plotly_chart(fig_frequency, use_container_width=True)

with c3:
    st.plotly_chart(fig_monetary, use_container_width=True)

st.caption("Abiyyu Muflih Kurnia")
st.caption("© My Collection 2025")


