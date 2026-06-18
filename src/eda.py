import pandas as pd

from db import engine

query = """SELECT * FROM hotel_revenue;"""

df=pd.read_sql(query,engine)

print(df.head())
print(df.shape)
print(df.isnull().sum())


df['children']= df['children'].replace('NA',0)
print(df['children'].unique())
df['children']=df['children'].astype(int)
print(df['children'].unique())


df['agent']= df['agent'].replace('NULL',0)
df['company']= df['company'].replace('NULL',0)

print(df['agent'].unique())
print(df['company'].unique())

df['total_revenue']=df['adr']*(df['stays_in_week_nights']+df['stays_in_weekend_nights'])
print(df['total_revenue'].head(10))
print(df['total_revenue'].describe())

print(df[df['adr'] < 0]['adr'].count())
print(df[df['adr'] < 0][['hotel', 'adr', 'total_revenue']].head())
df=df[df['adr']>=0]
print(df[df['adr'] < 0]['adr'].count())
print(df['total_revenue'].describe())

df.to_sql('hotel_cleaned',engine,if_exists='replace',index=False)