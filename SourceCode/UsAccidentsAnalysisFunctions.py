####################################################################################################################################################################################
# Import Dependencies:
####################################################################################################################################################################################

# Import Python Dependencies
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Import configurations
from Configs import inputFileName
from Configs import inputFilePath
from Configs import outputFilePath


####################################################################################################################################################################################
# Function(s) Definitions:
####################################################################################################################################################################################


# These functions ae used in the main script file(s)


####################################################################################################################################################################################
# Function: Get input file 
####################################################################################################################################################################################
def getInputFile():
    inputFile = inputFilePath + inputFileName
    print("Input file is: " + inputFile)
    return inputFile

####################################################################################################################################################################################
# Function: Get initial data from input file as dataframe  
####################################################################################################################################################################################
def getInputData(inputFile: str) -> pd.DataFrame:
    inputDF = pd.read_csv(inputFile)
    print("Dataframe created")
    return inputDF

####################################################################################################################################################################################
# Function: Cleanup initial data from input file  
####################################################################################################################################################################################
def cleanInputData(inputDF: pd.DataFrame) -> pd.DataFrame:
    
    
    # Save counts for later analysis
    columnCountBeforeCleanup = len(inputDF.columns)
    rowCountBeforeCleanup = inputDF['ID'].count()
    
    # Remove columns not being used for analysis
    inputDF.drop(columns=['End_Lat', 'End_Lng', 'End_Time', 'Distance(mi)', 'Number', 'Street', \
                          'Side', 'Wind_Chill(F)', 'Wind_Direction', 'Civil_Twilight', \
                          'Nautical_Twilight', 'Astronomical_Twilight', 'Temperature(F)', \
                          'Humidity(%)', 'Pressure(in)', 'Visibility(mi)'], inplace=True)

    # Remove any rows with all columns na/null
    inputDF.dropna(how = 'all', inplace=True)
    
    # For columns being analysed - remove any rows that have na/null value as it cannot be aggregated
    # These columns are: ID, State, Start_Time, Start_Lat, Start_Lng, Timezone, Weather_Condition, Sunrise_Sunset 
    inputDF.dropna(subset=['ID', 'State', 'Start_Time', 'Start_Lat', 'Start_Lng', 'Timezone', 'Weather_Condition', 'Sunrise_Sunset'], inplace=True)

    # Save counts for later analysis (if needed)
    columnCountAfterCleanup = len(inputDF.columns)
    rowCountAfterCleanup = inputDF['ID'].count()

    columnsDeleted = columnCountBeforeCleanup-columnCountAfterCleanup 
    rowsDeleted = rowCountBeforeCleanup-rowCountAfterCleanup
    # Print counts of cleanup
    print("Clean up done, Number of columns deleted: {}, Number of rows deleted: {}".format(columnsDeleted, rowsDeleted))

    return inputDF

####################################################################################################################################################################################
# Function: Add date columns to the dataframe  
####################################################################################################################################################################################
def addDateColumns(inputDF: pd.DataFrame) -> pd.DataFrame:

    # Add columns for Month, Hour & Weekday
    inputDF['Month']=pd.to_datetime(inputDF['Start_Time']).dt.month
    inputDF['Hour']=pd.to_datetime(inputDF['Start_Time']).dt.hour
    inputDF['Weekday']=pd.to_datetime(inputDF['Start_Time']).dt.weekday_name

    # Print columns added
    print("Added required date columns to the dataframe")

    return inputDF

####################################################################################################################################################################################
# Function: Analyze by Timezone  
####################################################################################################################################################################################
def accidentsByTimezone(inputDF: pd.DataFrame):
    
    outputFileSubPath = 'ByTimezone/'

    # Get unique timezones & counts
    timezonesCounts = inputDF['Timezone'].value_counts().tolist()
    timezonesLabels = inputDF['Timezone'].value_counts().index.tolist()
    # Set colors for timezones
    timezonesGraphColors = ['royalblue', 'darkorange', 'gold', 'darkolivegreen']


    # 1. Count(s) of accidents by timezone


    # 1.1. Pie Chart (Counts by timezone)
    # Set the plot attributes & Plot the Pie chart
    pieExplode = (0.05, 0, 0, 0)    
    plt.figure(figsize=(12, 8))
    plt.axis("equal")
    plt.pie(timezonesCounts, explode=pieExplode, colors=timezonesGraphColors, labels=timezonesLabels,
        autopct="%1.1f%%", shadow=True, startangle=135)
    plt.title("Accidents in Different Timezone")
    # Save output file
    outputFile = outputFilePath + outputFileSubPath + 'Timezone_Accidents_Counts_Pie.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)


    # 1.2. Bar Chart (Counts by timezone)
    # Set the plot attributes & Plot the Bar chart
    plt.figure(figsize=(12, 8))
    # X-Axix limits & label: 
    plt.xlim(-0.75, len(timezonesLabels)-0.25)
    plt.xlabel("Timezone")
    xlocs, xlabs = plt.xticks()
    # xlocs=[i+1 for i in range(0,len(timezonesLabels))]
    # xlabs=[i/2 for i in range(0,len(timezonesLabels))]
    xlocs=[i for i in range(0,len(timezonesLabels))]
    xlabs=timezonesLabels
    plt.xticks(xlocs, xlabs)
    # Y-Axis limits & label
    plt.ylim(0, max(timezonesCounts)+200000)
    plt.ylabel("Count of Accident(s)")
    # Plot the chart
    plt.bar(timezonesLabels, timezonesCounts, color=timezonesGraphColors, alpha=0.5, align="center")
    plt.title("Accidents in Different Timezone")
    # put value labes for Y-Axis 
    for i, v in enumerate(timezonesCounts):
        # Tip: Adjust -0.10 & +0.01 for positioning the lable text in the bar column
        plt.text(xlocs[i] -0.10, v + 0.01, str(v))
    # Save output file 
    outputFile = outputFilePath + outputFileSubPath + 'Timezone_Accidents_Counts_Bar.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)



    # 2. Average severity pf accident by Timezone

    # Empty lists for bar chart to be plotted
    timezonesAvgSev = []
    
    # Extract mean (avg) sev for each timezone:
    for tz in timezonesLabels:
        meanSev = inputDF[inputDF['Timezone'] == tz]['Severity'].mean()
        timezonesAvgSev.append(round(meanSev,3))

    # Set the plot attributes & Plot the Bar chart
    # X-Axix limits & label: 
    plt.xlim(-0.75, len(timezonesLabels)-0.25)
    plt.xlabel("Timezone")
    xlocs, xlabs = plt.xticks()
    xlocs=[i+1 for i in range(0,len(timezonesAvgSev))]
    xlabs=[i/2 for i in range(0,len(timezonesAvgSev))]
    plt.xticks(xlocs, xlabs)
    # Y-Axis limits & label
    plt.ylim(0, max(timezonesAvgSev)+0.500)
    plt.ylabel("Avergare Severity of Accident")
    # Plot the chart:
    plt.figure(figsize=(12, 8))
    plt.bar(timezonesLabels, timezonesAvgSev, color=timezonesGraphColors, alpha=0.5, align="center")
    plt.title("Average Accidents Severity in Different Timezone")
    # put value labes for Y-Axis 
    for i, v in enumerate(timezonesAvgSev):
        # Tip: Adjust -1.10 & +0.01 for positioning the lable text in the bar column
        plt.text(xlocs[i] -1.10, v + 0.01, str(v))
 
    # Define & Save: Output file - Pie chart
    outputFile = outputFilePath + outputFileSubPath + 'Timezone_Accidents_AvgSev_Bar.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)

####################################################################################################################################################################################
