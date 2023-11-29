import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

df = pd.read_csv("./data.csv")
df.sort_values(by="datetime", inplace=True)
df.reset_index(inplace=True)

df['datetime'] = pd.to_datetime(df['datetime'])

min_date = df["datetime"].min()
max_date = df["datetime"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

df = df[(df["datetime"] >= str(start_date)) &
        (df["datetime"] <= str(end_date))]
average_demand_by_season = df.groupby(
    'season')['total_count'].mean().reset_index()
df['day_type'] = df['workingday'].apply(
    lambda x: 'Working Day' if x == 'Yes' else 'Weekend')
hourly_rentals_by_daytype = df.groupby(['day_type', 'hour'])[
    'total_count'].mean().reset_index()

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Variasi Permintaan Sewa per Musim')

fig, ax = plt.subplots(figsize=(16, 8))
plt.bar(average_demand_by_season['season'],
        average_demand_by_season['total_count'])
plt.title('Rata-rata Permintaan Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.subheader('Pola Penyewaan Sepeda Antara Hari Kerja dan Akhir Pekan')
fig, ax = plt.subplots(figsize=(16, 8))
plt.plot(hourly_rentals_by_daytype[hourly_rentals_by_daytype['day_type'] == 'Working Day']['hour'],
         hourly_rentals_by_daytype[hourly_rentals_by_daytype['day_type']
                                   == 'Working Day']['total_count'],
         label='Working Day', marker='o')
plt.plot(hourly_rentals_by_daytype[hourly_rentals_by_daytype['day_type'] == 'Weekend']['hour'],
         hourly_rentals_by_daytype[hourly_rentals_by_daytype['day_type']
                                   == 'Weekend']['total_count'],
         label='Weekend', marker='o')
plt.title('Rata-rata Penyewaan Sepeda per Jam pada Hari Kerja dan Akhir Pekan')
plt.xlabel('Jam')
plt.ylabel('Rata-rata')
plt.legend()
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)
