import pandas as pd

from db import engine

query = """SELECT * FROM hotel_cleaned;"""

df=pd.read_sql(query,engine)
print(df.head())
print(df.shape)

# Bookings Trends & YOY % Grwoth

confirmed =df[df['is_canceled']==0]
print(confirmed.head(5))

yearly_booking=confirmed.groupby('arrival_date_year')['is_canceled'].count().reset_index()

print(yearly_booking.head(5))
yearly_booking.columns=['Year','Total_Bookings']
yearly_booking['YOY_Growth']=round(yearly_booking['Total_Bookings'].pct_change()*100,2)
print(yearly_booking)

# Q2

hotel_cancel= df.groupby('hotel').agg(
    Total_Bookings=('is_canceled','count'),
    Cancelled=('is_canceled','sum')
).reset_index()
print(hotel_cancel)

hotel_cancel['Cancellation%']=round((hotel_cancel['Cancelled']/hotel_cancel['Total_Bookings'])*100,2)
cancelled=df[df['is_canceled']==1]
Lost_Revenue=cancelled.groupby('hotel')['total_revenue'].sum().reset_index()
Lost_Revenue.columns=['hotel','Lost_Revenue']
hotel_cancel=hotel_cancel.merge(Lost_Revenue,on='hotel')

print(hotel_cancel)

# Country booking volume and cancellation rate
country_stats = df.groupby('country').agg(
    Total_Bookings=('is_canceled','count'),
    Cancellations=('is_canceled','sum')
).reset_index()
country_stats['Cancellation_Rate'] = round((country_stats['Cancellations'] / country_stats['Total_Bookings']) * 100, 2)

country_stats = country_stats.sort_values('Total_Bookings', ascending=False)
cancelled = df[df['is_canceled'] == 1]
country_lost = cancelled.groupby('country')['total_revenue'].sum().reset_index()
country_lost.columns = ['country', 'Lost_Revenue']
country_stats = country_stats.merge(country_lost, on='country')
print(country_stats.head(10))
# Q4 Repeated vs new guests value comparison
guest_stats=df.groupby('is_repeated_guest').agg(
    adr=('adr','mean'),
    Average_Revenue=('total_revenue','mean'),
    Total_Bookings=('is_canceled','count'),
    Cancellations=('is_canceled','sum')
).reset_index()

guest_stats['Cancellation_Rate'] = round((guest_stats['Cancellations'] / guest_stats['Total_Bookings']) * 100, 2)
print(guest_stats)
# Q5 Market Segment Quality Analysis
market_stats=df.groupby('market_segment').agg(
    avg_adr=('adr','mean'),
    avg_revenue=('total_revenue','mean'),
    Total_Bookings=('is_canceled','count'),
    cancellations=('is_canceled','sum')
    ).sort_values('Total_Bookings', ascending=False).reset_index()
cancelled = df[df['is_canceled']==1].groupby('market_segment')['is_canceled'].count().reset_index()
market_stats['Cancellation_Rate'] = round(market_stats['cancellations'] / market_stats['Total_Bookings'] * 100, 2)
print(market_stats)