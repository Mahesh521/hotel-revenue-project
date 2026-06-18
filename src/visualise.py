import pandas as pd
import matplotlib.pyplot as plt
from db import engine
import seaborn as sns
import numpy as np
query = """SELECT * FROM hotel_cleaned;"""

df=pd.read_sql(query,engine)
print(df.shape)
sns.set_theme(style="white", rc={
    "axes.grid": False,
    "axes.facecolor": "white",
    "figure.facecolor": "white"
})
#sns.despine()
#Chart1- Cancellation Rate by Hotel Type
hotel_cancel= df.groupby('hotel').agg(
    Total_Bookings=('is_canceled','count'),
    Cancelled=('is_canceled','sum')
).reset_index()
hotel_cancel['Cancellation%']=round((hotel_cancel['Cancelled']/hotel_cancel['Total_Bookings'])*100,2)
plt.figure(figsize=(10, 6))
sns.barplot(data=hotel_cancel, x='hotel', y='Cancellation%')
plt.title('Cancellation Rate by Hotel Type')
plt.xlabel('Hotel Type')
plt.ylabel('Cancellation Rate (%)')
plt.savefig('output/chart1_cancellations_in_hotels.png', dpi=150, bbox_inches='tight')
plt.show()
# Chart2- Trend of Bookingd over the Years
conditions=[
    df['arrival_date_month'].isin(['January','February','March']),
    df['arrival_date_month'].isin(['April','May','June']),
    df['arrival_date_month'].isin(['July','August','September']),
    df['arrival_date_month'].isin(['October','November','December'])
]
choices=['Q1','Q2','Q3','Q4']
df['Quarter']=np.select(conditions,choices,default='Unknown')
df['Period']=df['arrival_date_year'].astype(str)+' ' +df['Quarter']
confirmed=df[df['is_canceled']==0]
Total_Bookings=confirmed.groupby('Period')['is_canceled'].count().reset_index()
Total_Bookings.columns=['Period','Total_Bookings']
plt.figure(figsize=(12, 6))
sns.lineplot(data=Total_Bookings, x='Period', y='Total_Bookings', marker='o')
plt.title('Trend of Bookings over the Years')
plt.xlabel('Period')
plt.ylabel('Total Bookings')
plt.savefig('output/chart2_quarterly_trend_bookings.png', dpi=150, bbox_inches='tight')
plt.show()

# Top 10 Countries by Number of Bookings
confirmed = df[df['is_canceled']==0]
#reservation=df[df['reservation_status']=='Check-Out']
Confirmed_Reservations=confirmed[confirmed['reservation_status']=='Check-Out']
top_countries=Confirmed_Reservations.groupby('country').agg(
    Confirmed_Bookings=('is_canceled','count')
).reset_index().sort_values(by='Confirmed_Bookings',ascending=False).head(10)
print(top_countries)
top_countries=top_countries.sort_values(by='Confirmed_Bookings',ascending=True)
print(top_countries)
plt.figure(figsize=(10, 6))
plt.barh(data=top_countries, y='country', width='Confirmed_Bookings', color='skyblue')
for position, (index, row) in enumerate(top_countries.iterrows()):
    country=row['country']
    bookings=row['Confirmed_Bookings']
    plt.text(bookings+300,position,bookings)
    print(f"Country: {country}, Confirmed Bookings: {bookings}")
plt.title('Top 10 Countries by Number of Confirmed Bookings')
plt.xlabel('Number of Confirmed Bookings')
plt.ylabel('Country')
plt.tight_layout()
plt.savefig('output/chart3_top_10_countries.png', dpi=150, bbox_inches='tight')
plt.show()

# Chart4 Market Segment analysis

Market_stats=df.groupby('market_segment').agg(
    Total_Bookings=('is_canceled','count'),
    Cancelled=('is_canceled','sum'),
    Average_Revenue=('adr','mean')
).sort_values('Average_Revenue',ascending=False).reset_index()
Market_stats['Cancellation %']=round((Market_stats['Cancelled']/Market_stats['Total_Bookings'])*100,2)
x=np.arange(len(Market_stats))
print(Market_stats)
width=0.4
fig, ax1=plt.subplots()
bar1=ax1.bar(x-width/2,Market_stats['Cancellation %'],width=0.4, color='green', label='Cancellation %')
#ax1.legend(loc='upper right')
ax2=ax1.twinx()
bar2=ax2.bar(x+width/2,Market_stats['Average_Revenue'],width=0.4, color='orange',label= 'Average_Revenue')
#ax2.legend(loc='upper left')
ax1.set_ylabel('Cancellation %')
ax2.set_ylabel('Average Revenue')
ax1.legend([bar1, bar2], ['Cancellation %', 'Average_Revenue'], loc='upper right')
ax1.set_xticks(x)
ax1.set_xticklabels(Market_stats['market_segment'])
plt.title('Market Segment analysis')
plt.savefig('output/chart4_market_segment_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

# Chart5 Repeated Guests vs New Guests
guest_stats=df.groupby('is_repeated_guest').agg(
    Average_ADR=('adr','mean'),
    Total_Bookings=('is_canceled','count'),
    Cancellations=('is_canceled','sum')
).reset_index()
guest_stats['Cancellation %']=round((guest_stats['Cancellations']/guest_stats['Total_Bookings'])*100,2)
guest_stats['is_repeated_guest']=guest_stats['is_repeated_guest'].replace({0:'New',1:'Repeated'})
fig, axes =plt.subplots(1,2, figsize=(12,6))
axes[0].bar(guest_stats['is_repeated_guest'],guest_stats['Cancellation %'],color='red')
axes[0].set_title('Cancellations: Repeated vs New Guests')
axes[0].set_ylabel('Cancellation Rate (%)')
axes[1].bar(guest_stats['is_repeated_guest'],guest_stats['Average_ADR'],color='green')
axes[1].set_title('Average ADR: Repeated vs New Guests')
axes[1].set_ylabel('Average ADR')
plt.tight_layout()
plt.savefig('output/chart5_repeated_vs_new_guests.png', dpi=150, bbox_inches='tight')
plt.show()
