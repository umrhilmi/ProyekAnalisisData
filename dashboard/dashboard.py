import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

bike_df = pd.read_csv("dashboard/main_data.csv")

def create_weather_situation_df(df):
    return df.groupby(by="weathersit").cnt.mean().reset_index().rename(columns={"weathersit": "Weather Condition"})

def create_weekday_df(df):
    return df.groupby(by="weekday").cnt.mean().sort_values(ascending=False).reset_index()

def create_season_day_df(df):
    return df.groupby(by="season").agg({"casual": "mean", "registered": "mean"})

def create_holiday_df(df):
    holiday_df = df.groupby("holiday").cnt.mean().reset_index()
    holiday_df["holiday"] = holiday_df["holiday"].replace({0: "Not Holiday", 1: "Holiday"})
    return holiday_df

bike_df["yr"] = bike_df["yr"].replace({0: 2011, 1: 2012})

st.sidebar.header("🔍 Filter Data")
unique_years = sorted(bike_df["yr"].unique())
selected_year = st.sidebar.selectbox("Select Year:", ["All"] + [str(year) for year in unique_years])
selected_season = st.sidebar.multiselect("Select Season(s):", ["All", "Spring", "Summer", "Fall", "Winter"])

filtered_df = bike_df.copy()
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["yr"] == int(selected_year)]

season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
filtered_df["season"] = filtered_df["season"].map(season_map)
if "All" not in selected_season and selected_season:
    filtered_df = filtered_df[filtered_df["season"].isin(selected_season)]

weather_situation_df = create_weather_situation_df(filtered_df)
weekday_df = create_weekday_df(filtered_df)
season_day_df = create_season_day_df(filtered_df)
holiday_df = create_holiday_df(filtered_df)

st.header("🚴‍♂️ Bike Rental Dashboard")

# Grafik 1
st.subheader("Number of Bike Rentals per Season")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=filtered_df["season"], y=filtered_df["cnt"], palette="viridis", ax=ax)
ax.set_xlabel("Season")
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

# Grafik 2
st.subheader("Total Bike Rentals per Month")
month_trend = filtered_df.groupby("mnth")["cnt"].sum().reset_index()
month_labels = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}
month_trend["mnth"] = month_trend["mnth"].map(month_labels)
max_month = month_trend.loc[month_trend["cnt"].idxmax(), "mnth"]
colors = ["#2ca02c" if month == max_month else "#aec7e8" for month in month_trend["mnth"]]
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=month_trend["mnth"], y=month_trend["cnt"], palette=colors, ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

# Grafik 3
st.subheader("Monthly Bike Rental Comparison between 2011 and 2012")
fig, ax = plt.subplots(figsize=(12, 5))
bike_df.groupby(["yr", "mnth"]).cnt.sum().unstack().T.plot(kind="bar", ax=ax, color=["#FFB6C1", "#FF6347"])
ax.set_xlabel("Month")
ax.set_ylabel("Number of Rentals")
ax.legend(title="Year")
st.pyplot(fig)

# Grafik 4
st.subheader("Average Bike Rentals on Weekdays and Weekends")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=filtered_df["workingday"].map({0: "Weekend", 1: "Weekday"}), y=filtered_df["cnt"], palette="cubehelix", ax=ax)
ax.set_xlabel("Day Type")
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

st.markdown("---")
st.markdown("© 2025 **Umar Hilmi** | All rights reserved.")
