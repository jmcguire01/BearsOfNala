import pandas as pd
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt 
import statsmodels.api as sm 
import seaborn as sns

# date of March 25, 2020 is set as "end" as it is the first date of reliable case tracking
dEnd = date(2020,3,25)
# Calculate number of days since dEnd, and determine weeks
today = date.today()-timedelta(1)
dDiff = today - dEnd
weeks = dDiff.days//7
days = dDiff.days%7
p=1
dateArr = []
urlPath = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv')
while True:
    dt = (date.today()-timedelta(p)).strftime('%m-%d-%Y')
    dateArr.append(dt)
    p+=7
    if p == (7*(weeks+1)+1):
        break
urlArr = []
for i in dateArr:
    urlArr.append(urlPath.format(i))
state_names = [x.upper() for x in ["Alaska", "Alabama", "Arkansas", "American Samoa", 'Arizona', "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]]
dToday = (date.today()-timedelta(1)).strftime('%m-%d-%Y')
dPrior = (date.today()-timedelta(2)).strftime('%m-%d-%Y')
dfToday = pd.read_csv(urlPath.format(dToday))
dfPrior = pd.read_csv(urlPath.format(dPrior))
dfToday['Province_State'] = dfToday['Province_State'].str.upper()
dfToday['Admin2'] = dfToday['Admin2'].str.upper()
dfPrior['Province_State'] = dfPrior['Province_State'].str.upper()
dfPrior['Admin2'] = dfPrior['Admin2'].str.upper()
dfCounty = dfToday[dfToday['Province_State'].isin(state_names)]
countyArr = dfCounty['Admin2'].unique()

# Filter user focus to State vs County. Limits overlaps between where County == State
locInput = input("Please choose location of interest by either entering 'State' or 'County'").upper()
while True:
    if locInput == "STATE" or locInput == "COUNTY":
        break
    locInput = input("There was an error in your entry, please re-enter 'State; or 'County' based on your selection of interest").upper()


userInput = input("Please enter the location you wish to examine").upper()
d= {}
dfSelect = pd.DataFrame(d)
validEntry = [] # array to concatentate two arrays for user input to check if True
#creates arrays to hold state .sum() data
stateLoc = []
stateConf = []
stateDeaths = []
stateActive = []
stateDate = []
#holds data for the change per week
dfWkChange = pd.DataFrame(d)
indexPoints = []
dataPointsPos = []
dataPointsDeaths = []
dataPointsActive = []
for i in state_names:
    validEntry.append(i)
for i in countyArr:
    validEntry.append(i)
while userInput not in validEntry:
    userInput = input('No records are indicated based on your entry. Please check the spellinng of the location of interest and re-enter location').upper()

if locInput == 'COUNTY':
    if userInput in countyArr:
        for i in urlArr:
            df = pd.read_csv(i)
            df['Province_State'] = df['Province_State'].str.upper()
            df['Admin2'] = df['Admin2'].str.upper()
            df = df[df['Admin2']==userInput]
            dfSelect = dfSelect.append(df)
        for i in range (0,len(urlArr)):
            indexPoints.append(i)
        dfSelect['Index'] = indexPoints
        dfSelect = dfSelect.set_index('Index')
        dfSelect['Last_Update'] = pd.to_datetime(dfSelect.Last_Update)
        dfSelect['Last_Update'] = dfSelect['Last_Update'].dt.strftime('%m-%d-%Y')
        for i in range (0,len(urlArr)):
            if i+1 > (len(urlArr)-1):
                break
            else:
                testPosDelta = dfSelect.iat[i,7]-dfSelect.iat[i+1,7]
                dataPointsPos.append(testPosDelta)
                deathsDelta = dfSelect.iat[i,8]-dfSelect.iat[i+1,8]
                dataPointsDeaths.append(deathsDelta) 
                activeDelta = dfSelect.iat[i,10]-dfSelect.iat[i+1,10]
                dataPointsActive.append(activeDelta)
        dfWkChange['Increased Cases'] = dataPointsPos
        dfWkChange['Increased Deaths'] = dataPointsDeaths
        dfWkChange['Change Active Cases'] = dataPointsActive
        dfWkChange['Date of Change'] = dfSelect.iloc[0:len(urlArr)-1,4]

if locInput == 'STATE':
    if userInput in state_names:
        for i in urlArr:
            df = pd.read_csv(i)
            df['Province_State'] = df['Province_State'].str.upper()
            df['Admin2'] = df['Admin2'].str.upper()
            df = df[df['Province_State']==userInput]
            stateLoc.append(df['Province_State'].mode()[0])
            stateConf.append(df['Confirmed'].sum())
            stateDeaths.append(df['Deaths'].sum())
            stateDate.append(df['Last_Update'].mode()[0])
            stateActive.append(df['Active'].sum())
        for i in range (0,len(urlArr)):
            indexPoints.append(i)
        dfSelect['Index'] = indexPoints
        dfSelect = dfSelect.set_index('Index')
        dfSelect['Province_State'] = stateLoc
        dfSelect['Last_Update'] = stateDate 
        dfSelect['Confirmed'] = stateConf
        dfSelect['Deaths'] = stateDeaths
        dfSelect['Active Cases'] = stateActive
        dfSelect['Last_Update'] = pd.to_datetime(dfSelect.Last_Update)
        dfSelect['Last_Update'] = dfSelect['Last_Update'].dt.strftime('%m-%d-%Y')
        for i in range (0,len(urlArr)):
            if i+1 > (len(urlArr)-1):
                break
            else:
                testPosDelta = dfSelect.iat[i,2]-dfSelect.iat[i+1,2]
                dataPointsPos.append(testPosDelta)
                deathsDelta = dfSelect.iat[i,3]-dfSelect.iat[i+1,3]
                dataPointsDeaths.append(deathsDelta) 
                activeDelta = dfSelect.iat[i,4]-dfSelect.iat[i+1,4]
                dataPointsActive.append(activeDelta)
        dfWkChange['Increased Cases'] = dataPointsPos
        dfWkChange['Increased Deaths'] = dataPointsDeaths
        dfWkChange['Change Active Cases'] = dataPointsActive
        dfWkChange['Date of Change'] = dfSelect.iloc[0:len(urlArr)-1,1]

def dataReturn():
    if userInput in state_names:
        return dfWkChange
    elif userInput in countyArr:
        return dfWkChange

def recentData():
    if userInput in countyArr:
        tstDf2 = dfPrior[dfPrior['Admin2']==userInput]
        casesTotalLoc = dfSelect['Confirmed'][0]
        casesYesterday = int(tstDf2['Confirmed'])
        casesChangeToday = casesTotalLoc-casesYesterday
    elif userInput in state_names:
        tstDf2 = dfPrior[dfPrior['Province_State']==userInput]
        casesTotalLoc = stateConf[0]
        casesYesterday = tstDf2['Confirmed'].sum()
        casesChangeToday = casesTotalLoc-casesYesterday
    return "The total number cases in {} is {}, with an increase of {} from the day prior.".format(userInput,casesTotalLoc,casesChangeToday)


def dataGraph():
    x1 = dfWkChange['Date of Change'][::-1]
    y2 = dfWkChange['Increased Deaths'][::-1]
    y = dfWkChange['Increased Cases'][::-1]
    fig, ax1 = plt.subplots()
    
    color = 'blue'
    ax1.set_xlabel('Week Intervals Since 03-25-2020')
    ax1.set_ylabel('Cases per week')
    ax1.plot(x1,y, color=color)
    ax1.tick_params(axis='y',labelcolor=color)

    ax2 = ax1.twinx()

    color = 'red'
    ax2.set_ylabel('Deaths per Week', color=color)
    ax2.plot(x1,y2,color=color)
    ax2.tick_params(axis='y',labelcolor=color)

    fig.tight_layout()
    plt.grid(True)
    plt.title("Change of COVID-19 Cases Over Time for {}".format(userInput))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, fontsize=10)
    plt.show()
    
print(dataReturn(),"\n",
recentData(),"\n",
dataGraph())