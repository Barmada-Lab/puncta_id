#imports necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot


#_____________________beginning of user input______________________________
#specify the folder containing ROC_data.csv and the desired name for the spreadsheet that is outputted
PATH='/hard drive/experiment folder/'
file_input = PATH+'ROC_data.csv'
file_ouput = PATH+'ROC_table.csv'

#Just include high confidence aggregates? select either 'yes' or 'no'
high_con = 'no'
#specify the upper bound of CV values to assess
upper_bound = 2
#specify the number of CV thresholds between 0 and the upper bound to test
breaks = 200
#specify fluorescent channel
channel = 'Cy5'
#specify timepoint
timepoint = 1
#_____________________end of user input______________________________

#imports ROC_data.csv
df = pd.read_csv(file_input)

#counts the number of cells without aggregates
no_agg_num = len(list(df['aggregate'][df['aggregate'] == 0]))
#counts the number of cells with aggregates
aggs_num = len(list(df['aggregate'][df['aggregate'] > 0]))
#counts the number of cells with high confidence aggregates
high_con_aggs_num = len(list(df['aggregate'][df['aggregate'] == 2]))

#creates a list of all CV threshold values
thresh_list = [x*upper_bound/(breaks) for x in range(breaks)]
thresh_list.append(upper_bound)

#creates a new dataframe called df_ROC
df_ROC = pd.DataFrame()
#adds the thresh_list as a column to df_ROC
df_ROC['threshold'] = thresh_list

#creates subsetted dataframes containing either no aggregates, all aggregates, or high-confidence aggregates
df_no_agg = df[df['aggregate'] == 0]
df_agg = df[df['aggregate'] > 0]
df_high_con = df[df['aggregate'] == 2]

#creates lists that count how many cells have a CV value below each threshold value
no_aggs_list = [df_no_agg[channel+'-CV-'+str(timepoint)][df_no_agg[channel+'-CV-'+str(timepoint)]<x].count() for x in thresh_list]
aggs_list = [df_agg[channel+'-CV-'+str(timepoint)][df_agg[channel+'-CV-'+str(timepoint)]<x].count() for x in thresh_list]
high_con_list = [df_high_con[channel+'-CV-'+str(timepoint)][df_high_con[channel+'-CV-'+str(timepoint)]<x].count() for x in thresh_list]
#creates lists of false positive and true positive percentages for each threshold value
false_positive = [((no_agg_num-x)/no_agg_num)*100 for x in no_aggs_list]
true_positive = [((aggs_num-x)/aggs_num)*100 for x in aggs_list]
high_con_positive = [((high_con_aggs_num-x)/high_con_aggs_num)*100 for x in high_con_list]

#adds lists as columns to ROC dataframe
df_ROC['no_agg'] = no_aggs_list
df_ROC['agg'] = aggs_list
df_ROC['high_con_agg'] = high_con_list
df_ROC['false_positive'] = false_positive
df_ROC['true_positive'] = true_positive
df_ROC['high_con_positive'] = high_con_positive
df_ROC['diff'] = df_ROC['true_positive']+(100-df_ROC['false_positive'])
df_ROC['diff_high'] = df_ROC['high_con_positive']+(100-df_ROC['false_positive'])

#calculates the area under the curve
auc_all = str(np.round_(np.sum((np.array(false_positive[0:200])-np.array(false_positive[1:201]))*np.array(true_positive[0:200]))/10000,3))
auc_high_con = str(np.round_(np.sum((np.array(false_positive[0:200])-np.array(false_positive[1:201]))*np.array(high_con_positive[0:200]))/10000,3))

print(str(auc_all))

df_ROC.to_csv(file_ouput)
#calculates the optimal threshold values
max_diff = max(df_ROC['diff'])
calc_threshold = df_ROC[df_ROC['diff']==max_diff]['threshold']
optimal_x = df_ROC[df_ROC['diff']==max_diff]['false_positive']
optimal_y = df_ROC[df_ROC['diff']==max_diff]['true_positive']


max_diff_high = max(df_ROC['diff_high'])
calc_threshold_high = df_ROC[df_ROC['diff_high']==max_diff_high]['threshold']
optimal_x_high = df_ROC[df_ROC['diff_high']==max_diff_high]['false_positive']
optimal_y_high = df_ROC[df_ROC['diff_high']==max_diff_high]['high_con_positive']

#plots the ROC curve
xlab = 'False Positive Rate (100-specificity)'
ylab = 'True Positive Rate (sensitivity)'
if (high_con == 'yes'):
	title = ' AUC = ' + auc_high_con + ' Optimal CV threshold ='+str(list((calc_threshold_high))[0])
	plot.scatter(false_positive, high_con_positive)
	plot.scatter(optimal_x_high,optimal_y_high)
else:
	title = 'AUC = ' + auc_all + ' Optimal CV threshold ='+str(list((calc_threshold))[0])
	plot.scatter(false_positive, true_positive)
	plot.scatter(optimal_x,optimal_y)
plot.xlabel(xlab)
plot.ylabel(ylab)
plot.title(title)
plot.show()