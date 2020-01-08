####################################################################################################################################################################################
# Import Dependencies:
####################################################################################################################################################################################

# Import Python Dependencies
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

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
# Function: Analyze by Timezone  
####################################################################################################################################################################################
def accidentsByTimezone(inputDF: pd.DataFrame):
    
    # Get unique timezones & counts
    timezonesCounts = inputDF['Timezone'].value_counts()
    timezonesLabels = inputDF['Timezone'].value_counts().index.tolist()

    # 1. Count(s) of accidents by timezone

    # Set plot attributes such as explode, colors, & title
    pieExplode = (0.05, 0, 0, 0)    
    pieColors = ['royalblue', 'darkorange', 'gold', 'darkolivegreen']
    plt.title("Accidents in Different Timezone")
    # Plot the Pie chart
    plt.figure(figsize=(12, 8))
    plt.pie(timezonesCounts, explode=pieExplode, colors=pieColors, labels=timezonesLabels,
        autopct="%1.1f%%", shadow=True, startangle=135)
    plt.axis("equal")

    # Define & Save: Output file - Pie chart
    outputFile = outputFilePath + 'Timezone_Accidents_Counts_Pie.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)


    # 2. Average severity pf accident by Timezone

    # Empty lists for bar chart to be plotted
    barYAxisTimezonesAvgSev = []
    barXAxisTimezonesLabels = []

    # Extract mean (avg) sev for each timezone:
    for tz in timezonesLabels:
        meanSev = inputDF[inputDF['Timezone'] == tz]['Severity'].mean()
        barYAxisTimezonesAvgSev.append(round(meanSev,3))
        barXAxisTimezonesLabels.append(tz)

    # Set the bar chart attributes such as X-Axis, Y-Axis, colors etc.
    # colors
    barColors = ['royalblue', 'darkorange', 'gold', 'darkolivegreen']
    # title
    plt.title("Average Accidents Severity in Different Timezone")
    # X-Axix limits & label: 
    plt.xlim(-0.75, len(barXAxisTimezonesLabels)-0.25)
    plt.xlabel("Timezone")
    xlocs, xlabs = plt.xticks()
    xlocs=[i+1 for i in range(0,len(barYAxisTimezonesAvgSev))]
    xlabs=[i/2 for i in range(0,len(barYAxisTimezonesAvgSev))]
    plt.xticks(xlocs, xlabs)

    # Y-Axis limits & labll
    plt.ylim(0, max(barYAxisTimezonesAvgSev)+0.500)
    plt.ylabel("Avergare Severity of Accident")

    # Plot the bar chart:
    plt.figure(figsize=(12, 8))
    plt.bar(barXAxisTimezonesLabels, barYAxisTimezonesAvgSev, color=barColors, alpha=0.5, align="center")
    # put value labes for Y-Axis 
    for i, v in enumerate(barYAxisTimezonesAvgSev):
        plt.text(xlocs[i] -1.10, v + 0.01, str(v))
 
    # Define & Save: Output file - Pie chart
    outputFile = outputFilePath + 'Timezone_Accidents_AvgSev_Bar.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)


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
