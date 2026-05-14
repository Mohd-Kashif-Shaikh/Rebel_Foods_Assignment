import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Kitchen PNL Dashboard",layout="wide")
st.markdown("""
This dashboard provides interactive profitability and variance analysis for cloud kitchen stores across different cities and revenue cohorts. The dashboard helps identify operational efficiency, profitability drivers, discount impact, and food wastage trends.
""")
st.title("Cloud Kitchen PNL Dashboard")
st.markdown("Interactive Profitability & Variance Analysis Dashboard")
@st.cache_data #----for perfromace optiiation
def load_data():
    df=pd.read_csv("asg//data//processed_kitchen_pnl.csv")
    return df
df=load_data()
st.sidebar.header("Filters")
selected_month = st.sidebar.multiselect(
    "Select Month",
    options=df["MONTH"].unique(),
    default=df["MONTH"].unique()
)
selected_city = st.sidebar.multiselect(
    "Select City",
    options=df["CITY"].unique(),
    default=df["CITY"].unique()
)
selected_store = st.sidebar.multiselect(
    "Select Store",
    options=df["STORE"].unique(),
    default=df["STORE"].unique()
)
selected_revenue = st.sidebar.multiselect(
    "Revenue Cohort",
    options=df["REVENUE COHORT"].unique(),
    default=df["REVENUE COHORT"].unique()
)
selected_ebitda_category = st.sidebar.multiselect(
    "EBITDA Category",
    options=df["EBITDA CATEGORY"].unique(),
    default=df["EBITDA CATEGORY"].unique()
)
####SLIDERssss
revenue_range = st.sidebar.slider(
    "Revenue Range",
    float(df["NET REVENUE"].min()),
    float(df["NET REVENUE"].max()),
    (
        float(df["NET REVENUE"].min()),
        float(df["NET REVENUE"].max())
    )
)
ebitda_range = st.sidebar.slider(
    "EBITDA % Range",
    float(df["EBITDA_PCT"].min()),
    float(df["EBITDA_PCT"].max()),
    (
        float(df["EBITDA_PCT"].min()),
        float(df["EBITDA_PCT"].max())
    )
)
filtered_df = df[
    (df["MONTH"].isin(selected_month)) &
    (df["CITY"].isin(selected_city)) &
    (df["STORE"].isin(selected_store)) &
    (df["REVENUE COHORT"].isin(selected_revenue)) &
    (df["EBITDA CATEGORY"].isin(selected_ebitda_category)) &
    (df["NET REVENUE"].between(revenue_range[0], revenue_range[1])) &
    (df["EBITDA_PCT"].between(ebitda_range[0], ebitda_range[1]))
]

###KPI's Building
st.dataframe(filtered_df.head())
total_revenue = filtered_df["NET REVENUE"].sum()
total_ebitda = filtered_df["KITCHEN EBITDA"].sum()
avg_gm_pct = filtered_df["GM_PCT"].mean()
avg_ebitda_pct = filtered_df["EBITDA_PCT"].mean()
total_orders = filtered_df["ORDER COUNT"].sum()
avg_variance_pct = filtered_df["VARIANCE_PCT"].mean()
st.divider()
####################3
####Lapythoout
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
with col1:
    st.metric(
        "Total Revenue",
        f"₹ {total_revenue:,.0f}"
    )
with col2:
    st.metric(
        "Total EBITDA",
        f"₹ {total_ebitda:,.0f}"
    )
with col3:
    st.metric(
        "Avg GM %",
        f"{avg_gm_pct:.2f}%"
    )
with col4:
    st.metric(
        "Avg EBITDA %",
        f"{avg_ebitda_pct:.2f}%"
    )
with col5:
    st.metric(
        "Total Orders",
        f"{total_orders:,.0f}"
    )
with col6:
    st.metric(
        "Avg Variance %",
        f"{avg_variance_pct:.2f}%"
    )

tab1, tab2 = st.tabs([
    "Kitchen Level PNL",
    "Variance Analysis"
])
###Monthly revenue trend
st.divider()
st.subheader("Business Trends")
with tab1:
    col1, col2 = st.columns(2)
    # Revenue Trend Chart
    with col1:
        monthly_revenue = (
            filtered_df.groupby("MONTH")["NET REVENUE"]
            .sum()
            .reset_index()
        )
        fig1 = px.line(
            monthly_revenue,
            x="MONTH",
            y="NET REVENUE",
            markers=True,
            title="Monthly Revenue Trend"
        )
        st.plotly_chart(
            fig1,
            use_container_width=True
        )
    # EBITDA Trend Chart
    with col2:
        monthly_ebitda = (
            filtered_df.groupby("MONTH")["KITCHEN EBITDA"]
            .sum()
            .reset_index()
        )
        fig2 = px.line(
            monthly_ebitda,
            x="MONTH",
            y="KITCHEN EBITDA",
            markers=True,
            title="Monthly EBITDA Trend"
        )
        st.plotly_chart(
            fig2,
            use_container_width=True
        )
    st.divider()
    st.subheader("Store & City Performance")
    col3, col4 = st.columns(2)
    with col3:
        city_revenue = (
            filtered_df.groupby("CITY")["NET REVENUE"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig3 = px.bar(
            city_revenue,
            x="CITY",
            y="NET REVENUE",
            title="Revenue by City"
        )
        st.plotly_chart(
            fig3,
            use_container_width=True
        )
    with col4:
        top_stores = (
            filtered_df.groupby("STORE")["KITCHEN EBITDA"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig4 = px.bar(
            top_stores,
            x="KITCHEN EBITDA",
            y="STORE",
            orientation="h",
            title="Top 10 Stores by EBITDA"
        )
        st.plotly_chart(
            fig4,
            use_container_width=True
        )
    st.divider()
    st.subheader("Operational Insights")
    col5, col6 = st.columns(2)
    with col5:
        fig5 = px.scatter(
            filtered_df,
            x="DISCOUNT_PCT",
            y="EBITDA_PCT",
            color="CITY",
            hover_data=["STORE"],
            title="Discount % vs EBITDA %",
            trendline="ols"
        )
        st.plotly_chart(
            fig5,
            use_container_width=True
        )
    with col6:
        fig6 = px.scatter(
            filtered_df,
            x="VARIANCE_PCT",
            y="EBITDA_PCT",
            color="CITY",
            hover_data=["STORE"],
            title="Variance % vs EBITDA %",
            trendline="ols"
        )
        st.plotly_chart(
            fig6,
            use_container_width=True
        )
with tab2:
    st.subheader("Variance Level PNL Dashboard")
    selected_variance = st.multiselect(
        "Select Variance Category",
        options=filtered_df["VARIANCE_CATEGORY"].unique(),
        default=filtered_df["VARIANCE_CATEGORY"].unique()
    )
    variance_df = filtered_df[
        filtered_df["VARIANCE_CATEGORY"].isin(selected_variance)
    ]
    variance_summary = (
        variance_df.groupby("REVENUE COHORT")["VARIANCE_PCT"]
        .mean()
        .reset_index()
    )
    st.divider()
    fig7 = px.bar(
        variance_summary,
        x="REVENUE COHORT",
        y="VARIANCE_PCT",
        color="REVENUE COHORT",
        title="Average Variance % by Revenue Cohort"
    )
    st.plotly_chart(
        fig7,
        use_container_width=True
    )
    store_count = (
        variance_df.groupby(
            ["MONTH", "REVENUE COHORT"]
        )["STORE"]
        .nunique()
        .reset_index()
    )
    pivot_table = store_count.pivot(
        index="REVENUE COHORT",
        columns="MONTH",
        values="STORE"
    )
    st.divider()
    st.subheader("Store Count Matrix")
    st.dataframe(
        pivot_table,
        use_container_width=True
    )
    st.divider()
    #Heat map
    fig8 = px.imshow(
        pivot_table,
        text_auto=True,
        aspect="auto",
        title="Store Count Heatmap"
    )
    st.plotly_chart(
        fig8,
        use_container_width=True
    )
st.subheader("Detailed Data View")
st.dataframe(filtered_df,use_container_width=True)
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_kitchen_data.csv",
    mime="text/csv"
)
if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()
st.divider()
