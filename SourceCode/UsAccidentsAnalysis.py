####################################################################################################################################################################################
# Import Dependencies
####################################################################################################################################################################################

# Import Python Dependencies
import numpy as np

# Import functions
from UsAccidentsAnalysisFunctions import getInputFile
from UsAccidentsAnalysisFunctions import getInputData
from UsAccidentsAnalysisFunctions import cleanInputData
from UsAccidentsAnalysisFunctions import accidentsByTimezone
from UsAccidentsAnalysisFunctions import addDateColumns

####################################################################################################################################################################################
# Main logic
####################################################################################################################################################################################

# Get input file 
inputFile = getInputFile()

# Get initial input Data into a DataFrame

accidentsDataDF = getInputData(inputFile)

# Clean up the dataframe before further processing:
accidentsDataDF = cleanInputData(accidentsDataDF)

# Add the required date columns to the dataframe for further analysis
accidentsDataDF = addDateColumns(accidentsDataDF)

# Analyze & Chart the data

# Laury:
# Call Function - Analyze by Weather condition (DF as input)
# Call Function - Analyze by State (DF as input)

# Sumit:
# Call Function - Analyze by Time zone (DF as input)
accidentsByTimezone(accidentsDataDF)
# Call Function - Analyze by Month (DF as input)

# Doug:
# Call Function - Analyze by Day of the week (DF as input)
# Call Function - Analyze by Time of the day (DF as input)

