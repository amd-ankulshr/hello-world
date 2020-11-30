# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 19:35:01 2020


Trying date automation

@author: ankulshr
"""
import pandas as pd
import datetime
from pandas import ExcelWriter
import math
from pandas import ExcelFile
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns
import statistics
from statistics import stdev
import warnings
import itertools
warnings.filterwarnings("ignore")
import gc
import timeit

gc.collect()

###matplotlib import and settings

import matplotlib
import matplotlib.pyplot as plt
import statsmodels.api as sm
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['axes.titlesize'] = 40
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'
from matplotlib.pyplot import xticks
from matplotlib.pyplot import yticks

plt.style.use('Solarize_Light2')

#print(plt.style.available)




#Reading Data

#Alternate 1 : Through User nput
# usrin1 = input('enter dir locatio (Ex c:\\amd\\mydir\\data.xls): ')
# dfm = pd.read_excel(usrin1, sheet_name = "mon")

#Alternate 2 : In Program

dfm = pd.read_excel('C:\Anupam\AMD\MyMLProjects\AP Cash forecast_Brinda\my_analysis_new_scope_apr10_2020\Analysis and Data 66_3//AMD_APCash FC_66SeriesSet3_mq_Oct18.xlsx', sheet_name = "mon")


#Creating composit date column
filled = 27
#filled = int(input('enter number of filled rows (Ex : 100): '))
dfm1 = dfm[0:(filled-1)]

df1 = dfm1.copy()
df1 = df1.drop(df1.index[[0]])

df1.columns
df1["period"] = df1["Period/Series"].astype(str) + df1["Month"]

#################   DATE HANDLING #############
###############################################

#date input and processing
from datetime import date
from datetime import datetime
from time import strptime
import calendar
from dateutil.relativedelta import *

#CURRENT DATE
current_date = date.today()
current_time = datetime.now()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day


def dtchk(day, month,year,current_year):
    if year > current_year:
        print('\n',"Please mention current or past years")
    else:
        pass
        
    if month >12:
        print ('\n',"Please enter valid month")
    else:
        pass
    
    if day >31:
        print ('\n',"Please enter valid day")
    else:
        print('\n',"Thanks")    

#USER DATE ENTRIES
# date_entry = input('Enter start date for data intake [as Month,day (LAST DAY OF MONTH),year (Ex: 7,31,2017)] : ')
# month, day, year = map(int, date_entry.split(','))

#dtchk(day,month,year,current_year)


#DATE FROM DATA ALREADY READ
#Start Dates
yr_st = int(df1.iloc[0,0])
mnth_st = df1.iloc[0,1]    
mn_st = int(strptime(mnth_st,'%b').tm_mon)

dt_st = datetime(year=yr_st, month=mn_st, day=30)

#End Dates
yr_ed = int(df1.iloc[len(df1)-1,0])
mnth_ed = df1.iloc[len(df1)-1,1]    
mn_ed = strptime(mnth_ed,'%b').tm_mon

dt_ed = datetime(year=yr_ed, month=mn_ed, day=30)


#Processed date stamps
dt_fc = dt_ed+relativedelta(months=-2)

dt_r = dt_ed+relativedelta(months=+1)

#Considering later date (dataframe Vs User Input)           
# yr_st = max(yr_st,year)
# mn_st = max(mn_st,month)
'''
def mnincr1(mn,yr,n):
    if (mn+n > 12):
        mn1 = 1
        yr1 = yr+n
    else:
        mn1 = mn+1
        yr1 = yr
    return [mn1,yr1]

rdate = mnincr1(mn_ed,yr_ed)

progdt = str(mn)+"/"+str(30)+"/"+str(yr)
#progdt used for df01
rdt = str(rdate[0])+"/"+str(30)+"/"+str(rdate[1])
#rdt used for r,r1 etc
fc_st = 
'''

#################   DATE HANDLING END #############
###################################################


#------------
cat = {

"Series 1":"Ansys Inc.",
"Series 2":"Cadence Design Systems",

}


#Taking User inputs for series number 
#SELECTED SERIES 
#n = input('enter a series number (Ex Series 1): ')


opt = [
  "Series 1",
"Series 2",

]


l="Series 1"

   
str1 = cat[l]

#Coverting column name to Series name

df01 = df1[["period","WW", l]]           # selecting only specific series
df01["Values"] = df01[l].abs()        # converting column values to positive
df01 = df01.drop(l,axis = 1)        # dropping negative value column
df01['date'] = pd.date_range(start = dt_st, periods=len(df01), freq='M')


l1 = len(df01.index)
if l1 > 80:
    use = df01.iloc[l1-80:l1, :]
else:
    use = df01.copy()
    

use = use.reset_index(drop = True)
use.set_index("date", inplace = True)



l2 = len(use.index)
if l2 > 60:
    modl = use.iloc[0:math.ceil(0.75*l2), :]
    tst = use.iloc[(math.ceil(0.75*l2)):l2,:]
elif l2 > 45:
    modl = use.iloc[0:45,:]
    tst = use.iloc[(l2-45):l2,:]
else:
    modl = use.copy()
    tst = use.copy()
    
    
    
    
m = modl.Values.mean()
sd = stdev(modl["Values"])
   
 
modl.loc[modl["Values"]>=(m+3*sd) , "OValues"] = (m+3*sd)
modl.loc[modl["Values"]<=(m-3*sd) , "OValues"] = (m-3*sd)
modl.loc[(modl["Values"]<(m+3*sd)) & (modl["Values"]>(m-3*sd))  , "OValues"] = modl["Values"]   

m1 = tst.Values.mean()
sd1 = stdev(tst.Values[0:])
   

tst.loc[tst["Values"]>=(m1+3*sd1) , "OValues"] = (m1+3*sd1)
tst.loc[tst["Values"]<=(m1-3*sd1) , "OValues"] = (m1-3*sd1)
tst.loc[(tst["Values"]<(m1+3*sd1)) & (tst["Values"]>(m1-3*sd1))  , "OValues"] = tst["Values"] 




m2 = use.Values.mean()
sd2 = stdev(use.Values[0:])
 

use.loc[use["Values"]>=(m2+3*sd2) , "OValues"] = (m2+3*sd2)
use.loc[use["Values"]<=(m2-3*sd2) , "OValues"] = (m2-3*sd2)
use.loc[(use["Values"]<(m2+3*sd2)) & (use["Values"]>(m2-3*sd2))  , "OValues"] = use["Values"]



#------------------


import statsmodels.tsa as ts
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from numpy import log
from pylab import rcParams


mot = modl.copy()

#adding rows to dataframe
mot1 = mot.copy()
mot1 = mot1.replace(to_replace = 0, value = 1)
#mot1['Forecast'] = np.nan
collist = ['date','period', 'WW', 'Values', 'OValues']
rl = pd.DataFrame(columns = collist)
rl['date'] = pd.date_range(dt_r, periods=6, freq='M')
rl.set_index('date', inplace = True)
rslt = pd.concat([mot1,rl], axis = 0)   #reserve
rslt1 = pd.concat([mot1,rl], axis = 0)  #for SMA models
rslt2 = pd.concat([mot1,rl], axis = 0)  #for EWA models
rslt3 = pd.concat([mot1,rl], axis = 0)  #for Naive models
rslt4 = pd.concat([mot1,rl], axis = 0)

outfc = pd.DataFrame(columns = None)
outfc['ColIndex'] = pd.date_range(dt_fc, periods=4, freq='M')
outfc.set_index('ColIndex', inplace = True)
outfc['Run Details'] = ['Forecast Month 1','Forecast Month 2','Forecast Month 3','Error']
