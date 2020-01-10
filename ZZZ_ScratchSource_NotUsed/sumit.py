# Import Dependencies
import pandas as pd
import numpy as np
import datetime as dt

inputFile = './US_Accidents.csv'
inputDF = pd.read_csv(inputFile)


inputDF.dropna(subset=['ID', 'State', 'Start_Time', 'Start_Lat', 'Start_Lng', 'Timezone', 'Weather_Condition', 'Sunrise_Sunset'], inplace=True)
# Keep only rows that are for year 2017 & 2018 (data for other years is not consistent):
# Drop data less than 2017
indexDatesDrop = inputDF[ inputDF['Start_Time'] < '2017-01-00 00:00:00' ].index
inputDF.drop(indexDatesDrop , inplace=True)
# Drop data more that 2018
indexDatesDrop = inputDF[ inputDF['Start_Time'] > '2018-12-31 23:59:59' ].index
inputDF.drop(indexDatesDrop , inplace=True)


sevList = inputDF['Severity'].value_counts().index.tolist()
sevCounts = inputDF['Severity'].value_counts().tolist()
print(sevList)
print(sevCounts)


timezoneList = inputDF['Timezone'].value_counts().index.tolist()
for tz in timezoneList:
    print(tz)
    sevList = inputDF[inputDF['Timezone'] == tz]['Severity'].value_counts(dropna=False).sort_index().index.tolist()
    sevCounts = inputDF[inputDF['Timezone'] == tz]['Severity'].value_counts(dropna=False).sort_index().tolist()
    print(sevList)
    print(sevList[0])
    print(type(sevList[0]))
    print(sevCounts)


minDate = inputDF['Start_Time'].min()
maxDate = inputDF['Start_Time'].max()

print(minDate)
# 2015-03-09 07:00:00
# Delete any LT 2015-04-01 00:00:01
print(maxDate)
# 2019-04-01 03:26:00
# Delete any GT 2019-03-31 23:59:59

# Add columns for Month, Hour & Weekday
inputDF['Year']=pd.to_datetime(inputDF['Start_Time']).dt.year
inputDF['Year-Month']=pd.to_datetime(inputDF['Start_Time']).dt.to_period('M')
inputDF['Month']=pd.to_datetime(inputDF['Start_Time']).dt.month
inputDF['Hour']=pd.to_datetime(inputDF['Start_Time']).dt.hour
inputDF['Weekday']=pd.to_datetime(inputDF['Start_Time']).dt.weekday_name


print("Months:")
print(inputDF['Year'].value_counts())
print(inputDF['Year-Month'].value_counts())


print("State:")
print(inputDF['State'].value_counts().sort_index().index.tolist())
print(inputDF['State'].value_counts().sort_index().tolist())


