# Import Dependencies
import pandas as pd
import numpy as np


inputFile = './US_Accidents.csv'
inputDF = pd.read_csv(inputFile)

print(inputDF.head())
print(inputDF.dtypes.value_counts())
print(inputDF.info())

inputDF.dropna(how='all', inplace=True)

inputDF.dropna(subset=['Severity'], inplace=True)

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




    



