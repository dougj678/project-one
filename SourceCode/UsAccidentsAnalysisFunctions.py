####################################################################################################################################################################################
# Import Dependencies:
####################################################################################################################################################################################

# Import Python Dependencies
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Import configurations & global data
from Configs import inputFileName
from Configs import inputFilePath
from Configs import outputFilePath
from Configs import numOfYears
from Configs import timezonePopulationDict

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



    # 1. Pie Chart (Count(s) of Accidents by timezone)
    # Set the plot attributes & Plot the Pie chart
    pieExplode = (0.05, 0, 0, 0)    
    plt.figure(figsize=(12, 8))
    plt.axis("equal")
    plt.pie(timezonesCounts, explode=pieExplode, colors=timezonesGraphColors, labels=timezonesLabels,
        autopct="%1.1f%%", shadow=True, startangle=135)
    plt.title("Accidents in Different Timezone")
    # Save output file
    outputFile = outputFilePath + outputFileSubPath + 'Timezone_Accidents_1_Counts_Pie.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)



    # 2. Bar Chart (Counts by timezone)
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
    outputFile = outputFilePath + outputFileSubPath + 'Timezone_Accidents_2_Counts_Bar.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)



    # 3. Average severity pf accident by Timezone

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
    outputFile = outputFilePath + outputFileSubPath + 'Timezone_Accidents_3_AvgSev_Bar.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)

    

    # 4. Weighted Severity Index per 1000 accidents by Timezone
    # Severity = 0, 1, 2, 3, 4
    # Severity Weights = 10, 20, 40, 80, 160 (Total Weight = 310)
    # Total Weighted Severity = ((Count of 0 Sev * 10) + (Count of 1 Sev * 10) + (Count of 2 Sev * 20) + (Count of 3 Sev * 30) + (Count of 4 Sev * 40))/(Total Weight = 310)
    # Weighted Severity Index = Total Weighted Severity / Total Count of Accidents (in  Timezone)
    # Weighted Severity Index per 1000 accidents =  Weighted Severity Index * 1000

    # Empty lists for bar chart to be plotted
    timezonesWeigthedSevIndex = []

    # Severity weights 
    sevWeight = [10, 20, 40, 80, 160]
    # Extract mean (avg) sev for each timezone:
    for tz in timezonesLabels:
        sevList = inputDF[inputDF['Timezone'] == tz]['Severity'].value_counts(dropna=False).sort_index().index.tolist()
        sevCounts = inputDF[inputDF['Timezone'] == tz]['Severity'].value_counts(dropna=False).sort_index().tolist()
        
        ### For logging - Print the values 
        print(sevList)
        print(sevCounts)
        
        # Initialize calculated variables to 0 before calulcation per timezone
        # Weighted Severity Index per 1000 Accidents 
        weightedSevIndex = 0
        # Calculated Weighted Severity Index per Accident
        totalWeightedSevIndex = 0
        # Calculated Weighted Severity 
        weightedSev = 0
        # Calculated Total Weighted Severity 
        totalWeightedSev = 0
        # Count of Accidents by Timezone
        countByTimezone = 0        
        
        # for each severity found in timezone
        for i, sev in enumerate(sevList):
            totalWeightedSev = totalWeightedSev + (sevCounts[i] * sevWeight[sev])
            countByTimezone = countByTimezone + sevCounts[i]

        # Now have data per severity - calculate the final value for timezone
        weightedSev = totalWeightedSev/sum(sevWeight)
        totalWeightedSevIndex = weightedSev/countByTimezone 
        weightedSevIndex = round((totalWeightedSevIndex * 1000),2)
        timezonesWeigthedSevIndex.append(weightedSevIndex)

        ### For logging - Print the values 
        print(weightedSevIndex)
    
    # Done for all timezones

    ### For logging - Print the values 
    print(timezonesWeigthedSevIndex)

    # Set the plot attributes & Plot the Bar chart
    # X-Axix limits & label: 
    plt.xlim(-0.75, len(timezonesLabels)-0.25)
    plt.xlabel("Timezone")
    xlocs, xlabs = plt.xticks()
    xlocs=[i+1 for i in range(0,len(timezonesAvgSev))]
    xlabs=[i/2 for i in range(0,len(timezonesAvgSev))]
    plt.xticks(xlocs, xlabs)
    # Y-Axis limits & label
    plt.ylim(0, max(timezonesWeigthedSevIndex)+10.00)
    plt.ylabel("Weighted Severity Index per 1000 Accidents")
    # Plot the chart:
    plt.figure(figsize=(12, 8))
    plt.bar(timezonesLabels, timezonesWeigthedSevIndex, color=timezonesGraphColors, alpha=0.5, align="center")
    plt.title("Weighted Severity of Accidents in Different Timezone (per 1000 Accidents)")
    # put value labes for Y-Axis 
    for i, v in enumerate(timezonesWeigthedSevIndex):
        # Tip: Adjust -1.10 & +0.01 for positioning the lable text in the bar column
        plt.text(xlocs[i] -1.10, v + 0.01, str(v))
 
    # Define & Save: Output file - Pie chart
    outputFile = outputFilePath + outputFileSubPath + 'Timezone_Accidents_4_WeightedSevIndex_Bar.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)



    # 5. Bar Chart: Number of accidents by timezone per year per 1000 people
    # Count of Accidents by Timezone = Number of accidents per timezone in data analyzed
    # Count of Accidents by Timezone per year = Count of Accidents by Timezone / num of years of data being analyzed
    # Count of Accidents by Timezone per year per person = Count of Accidents by Timezone per year / population of timezone
    # Count of Accidents by Timezone per year per 1000 people = Count of Accidents by Timezone per year per person * 1000
    
    # Initialize variables used for calcuations:
    # List of Number of accidents per timezone per year per 1000 people
    timezoneCountsPerYearPer1000PopulationList = []
    
    # Get Accident per population * 1000 by Timezone in order as present in timezonesLabels
    for i, tz in enumerate(timezonesLabels):
 
        # Initialize variables used for calcuations:
        # Number of accidents per timezone per year 
        timezoneCountsPerYear = 0 
        # Number of accidents per timezone per year per person
        timezoneCountsPerYearPerPopulation = 0  
        # Number of accidents per timezone per year per 1000 people
        timezoneCountsPerYearPer1000Population = 0 

        # Perform the calulation 
        timezoneCountsPerYear = timezonesCounts[i]/numOfYears
        timezoneCountsPerYearPerPopulation = timezoneCountsPerYear / timezonePopulationDict[tz]
        timezoneCountsPerYearPer1000Population = round((timezoneCountsPerYearPerPopulation * 1000),3)

        # Add the calculated value to the list for the graph
        timezoneCountsPerYearPer1000PopulationList.append(timezoneCountsPerYearPer1000Population)


    # Calculations done - have the data now plot the bar chart  

    # Set the plot attributes & Plot the Bar chart
    plt.figure(figsize=(12, 8))
    # X-Axix limits & label: 
    plt.xlim(-0.75, len(timezonesLabels)-0.25)
    plt.xlabel("Timezone")
    xlocs, xlabs = plt.xticks()
    xlocs=[i for i in range(0,len(timezonesLabels))]
    xlabs=timezonesLabels
    plt.xticks(xlocs, xlabs)
    # Y-Axis limits & label
    plt.ylim(0, max(timezoneCountsPerYearPer1000PopulationList)+0.250)
    plt.ylabel("Accident(s) per 1000 People")
    # Plot the chart
    plt.bar(timezonesLabels, timezoneCountsPerYearPer1000PopulationList, color=timezonesGraphColors, alpha=0.5, align="center")
    plt.title("Accidents in Different Timezone per Population of 1000")
    # put value labes for Y-Axis 
    for i, v in enumerate(timezoneCountsPerYearPer1000PopulationList):
        # Tip: Adjust -0.10 & +0.01 for positioning the lable text in the bar column
        plt.text(xlocs[i] -0.10, v + 0.01, str(v))
    # Save output file 
    outputFile = outputFilePath + outputFileSubPath + 'Timezone_Accidents_5_Counts_1000_People_Bar.jpg'
    plt.savefig(outputFile)
    plt.close()
    print("Graph plotted: " + outputFile)



####################################################################################################################################################################################
