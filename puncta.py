import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#_____________________beginning of user input______________________________
#specify the folder containing ROC_data.csv and the desired names for the spreadsheets that are outputted
PATH='/hard drive/experiment_folder/'
exp_name = 'representative_experiment'
file_input = PATH+exp_name+'.csv'
punctas_ouput = PATH+exp_name+'_puncta.csv'
percent_output = PATH+exp_name+'_percent.csv'

#specify a CV threshold to use (determined with ROC curve)
threshold = 0.51
#specify the channel the images are in (i.e GFP, RFP, Cy5, DAPI)
channel = 'Cy5'

#_____________________end of user input______________________________
#imports the .csv file with experiment data as a dataframe
df = pd.read_csv(file_input)
#creates a new subsetted dataframe containing just columns corresponding to the CV values of the selected channel
df2 = df.filter(regex=channel+'-CV')
#creates a new dataframe-df_bool that assesses whether each CV value is above the threshold and assigns either True or False values
df_bool=df2>threshold
#creates an empty list called tps then populates this list with the timepoints found in column headers
tps = []
columns = df_bool.columns
for x in columns:
	tp = x[-1]
	tps.append(tp)

for x in tps:
	df_bool['tp-'+x]=int(tps[int(x)-1])
	df_bool['well-id']=df['well-id']
df_tps = df_bool.filter(regex = 'tp-').copy()
df_tps['last_tp'] = df['last_tp']
for col in df_tps.columns:
	df_tps['alive_'+col]=df_tps.loc[:,col]<df_tps.loc[:,'last_tp']+1
df_tps['well-id'] = df['well-id']
df_merged = df_bool.merge(df_tps)
df_alive = df_tps.filter(regex = 'alive_tp').copy()
df_alive['well-id'] = df['well-id']

for x in tps:
	df_merged['puncta_T'+x] = df_bool.iloc[:,int(x)-1]&df_alive.iloc[:,int(x)-1]

df_merged = df_merged.filter(regex='puncta_T')
df_merged['well-id'] = df['well-id']
df_merged = df_merged.merge(df_alive)
df = df.merge(df_merged)
df_sum = df.groupby('group').sum().reset_index()
df_sum_alive = df_sum.filter(regex='alive_tp')
df_sum_puncta =df_sum.filter(regex='puncta_T')
df_percent = df_sum[['group']].copy()

for x in tps:
	df_percent['percent'+x] = df_sum_puncta.iloc[:,int(x)-1].div(df_sum_alive.iloc[:,int(x)-1])*100
df.to_csv(punctas_ouput)
df_percent.to_csv(percent_output)

df_percent = df_percent.melt(id_vars = ['group'], var_name = 'time')
df_percent['time'] = df_percent['time'].str.replace(r'[a-z]', '').astype(int)
groups = df_percent['group'].unique()
for x in groups:
	plt.plot(df_percent[df_percent['group']==x]['time'],df_percent[df_percent['group']==x]['value'], label = x)
xlab = 'Timepoint'
ylab = '% of cells with puncta'
title = 'Puncta over time'
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(title)
plt.legend()
plt.show()