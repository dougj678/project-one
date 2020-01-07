# Import Dependencies
import pandas as pd
import numpy as np


inputFile = './US Accident Sample.csv'
inputDF = pd.read_csv(inputFile)

print(inputDF.head())
print(inputDF.get_dtype_counts())
print(inputDF.info())

inputDF.dropna(how='all', inplace=True)
print(inputDF.head())
print(inputDF.get_dtype_counts())
print(inputDF.info())

inputDF.dropna(subset=['Timezone'], inplace=True)

print(type(inputDF['Timezone'].value_counts()))

print(type(inputDF['Timezone'].unique()))
print(inputDF['Timezone'].unique())

Timezones = []
Counts = []
Timezones_Counts = inputDF['Timezone'].value_counts()
print(Timezones_Counts)
