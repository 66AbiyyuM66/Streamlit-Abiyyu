import pandas as pd
import matplotlib.pyplot as plt
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
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/mhvvn/dashboard_streamlit/refs/heads/main/img/tshirt.png", width=80)
    
    # Mengambil start_date & end_date dari date_input
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

st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_abiyyu.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_abiyyu.revenue.sum(), "AUD", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_abiyyu["order_date"],
    daily_orders_abiyyu["order_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.subheader("Best & Worst Performing Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_abiyyu.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_abiyyu.sort_values(by="quantity_x", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.subheader("Customer Demographics")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="customer_count", 
        x="gender",
        data=bygender_abiyyu.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Gender", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="customer_count", 
        x="age_group",
        data=byage_abiyyu.sort_values(by="age_group", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Age", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="state",
    data=bystate_abiyyu.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_abiyyu.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_abiyyu.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_abiyyu.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(y="recency", x="customer_id", data=rfm_abiyyu.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="frequency", x="customer_id", data=rfm_abiyyu.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="monetary", x="customer_id", data=rfm_abiyyu.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)

st.caption('Copyright (c) My Collection 2025')


