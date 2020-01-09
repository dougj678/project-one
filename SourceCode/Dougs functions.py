####################################################################################################################################################################################
# Function: Chart by Hour
####################################################################################################################################################################################

# Get unique hours & counts
HourCounts = inputDF['Hour'].value_counts()
HourLabels = inputDF['Hour'].value_counts().index.tolist()

#Plot the bar grapgh
plt.figure(figsize=(12, 8))
plt.bar(HourLabels, HourCounts, alpha=0.5, align="center")

# Set the bar chart attributes such as X-Axis, Y-Axis, colors etc.

# colors
barColors = ['royalblue']

# title
plt.title("Accidents by Hour of the Day")

# X-Axix limits & label: 
plt.xlim(-0.75, len(HourLabels)-0.25)
plt.xlabel("Hour")
xlocs, xlabs = plt.xticks()
xlocs=[i+0 for i in range(0,len(HourCounts))]
xlabs=[i+1 for i in range(0,len(HourCounts))]
plt.xticks(xlocs, xlabs)
plt.ylim(0, max(HourCounts)+0.500)
plt.ylabel("Count of Accidents")

# Define & Save: Output file - Bar chart
outputFile = outputFilePath + 'By hour of day.jpg'
plt.savefig(outputFile)
plt.close()

####################################################################################################################################################################################
# Function: Chart by Day of Week
####################################################################################################################################################################################

#Chart by day of the week

# Get unique hours & counts
WeekdayCounts = inputDF['Weekday'].value_counts()
WeekdayLabels = inputDF['Weekday'].value_counts().index.tolist()

#Plot the bar grapgh
plt.figure(figsize=(12, 8))
plt.bar(WeekdayLabels, WeekdayCounts, alpha=0.5, align="center")

# Set the bar chart attributes such as X-Axis, Y-Axis, colors etc.
# colors
barColors = ['royalblue']
# title
plt.title("Accidents by Day of the Week")

# X-Axix limits & label: 
plt.xlim(-0.75, len(WeekdayLabels)-0.25)
plt.xlabel("Weekday")
xlocs, xlabs = plt.xticks()
xlocs=[i+0 for i in range(0,len(WeekdayCounts))]
xlabs=[i+1 for i in range(0,len(WeekdayCounts))]
plt.xticks(xlocs, xlabs)
plt.ylim(0, max(WeekdayCounts)+10000)
plt.ylabel("Count of Accidents")

# Define & Save: Output file - Bar chart
outputFile = outputFilePath + 'By day of week.jpg'
plt.savefig(outputFile)
plt.close()

####################################################################################################################################################################################
# Function: Chart by Month of Year
####################################################################################################################################################################################

#Chart by month of the year

# Get unique hours & counts
MonthCounts = inputDF['Month'].value_counts()
MonthLabels = inputDF['Month'].value_counts().index.tolist()

#Plot the bar grapgh
plt.figure(figsize=(12, 8))
plt.bar(MonthLabels, MonthCounts, alpha=0.5, align="center")

# Set the bar chart attributes such as X-Axis, Y-Axis, colors etc.
# colors
barColors = ['royalblue']
# title
plt.title("Accidents by Month of the Year")

# X-Axix limits & label: 
plt.xlim(-0, len(MonthLabels)+.5)
plt.xlabel("Month")
xlocs, xlabs = plt.xticks()
xlocs=[i+1 for i in range(0,len(MonthCounts))]
xlabs=[i+1 for i in range(0,len(MonthCounts))]
plt.xticks(xlocs, xlabs)
plt.ylim(0, max(MonthCounts)+5000)
plt.ylabel("Count of Accidents")

# Define & Save: Output file - Bar chart
outputFile = outputFilePath + 'By month of year.jpg'
plt.savefig(outputFile)
plt.close()