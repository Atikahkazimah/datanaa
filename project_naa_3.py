# -*- coding: utf-8 -*-
"""Project_NAA_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b2kqAnmBOamUXfJzVQZW8QoHjNcdC3T4
"""

import pandas as pd
import numpy as np
import seaborn as sb
import plotly.express as px
import matplotlib.pyplot as plt

dfdata = pd.read_csv ('/content/NAA_Claims.csv')
dfdata.shape

dfdata.head()

dfdata.info()

dfdata.describe()

#claim status before rename
dfdata.groupby('CLAIM_STATUS').count()

#rename claim status
dfdata['CLAIM_STATUS'].replace({'Paid':'Approved'}, inplace=True)
dfdata['CLAIM_STATUS'].replace({'Auto Closed':'In Progress'}, inplace=True)
dfdata['CLAIM_STATUS'].replace({'Partially Paid':'Approved'}, inplace=True)
dfdata['CLAIM_STATUS'].replace({'Pending Assesment':'In Progress'}, inplace=True)
dfdata['CLAIM_STATUS'].replace({'Pending Documents':'In Progress'}, inplace=True)
dfdata['CLAIM_STATUS'].replace({'Closed':'In Progress'}, inplace=True)

#drop rows based on claim status cancelled
dfdata.drop(dfdata[dfdata['CLAIM_STATUS'] == "Cancelled"].index, inplace = True)

#drop column STATUS_TRACK_REGISTRATION and USER_ID
dfdata.drop(dfdata.iloc[:, 16:17], inplace=True, axis=1)
dfdata.groupby('CLAIM_STATUS').count()

#claim type before rename 
dfdata.groupby('CLAIM_TYPE').count()

#rename claim type
dfdata['CLAIM_TYPE'].replace({'Accidental Death Claim':'Death'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'Critical Illness/Dreaded Disease Claim':'Critical Illness'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'Death Claim':'Death'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'Death related to pregnancy':'Death'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'Funeral Expenses / Consolation Benefit Claim':'Funeral Expenses'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'Special Benefits On Female Plan':'Others'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'AIR weekly indemnity/surgical benefit ':'Others'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'Dismemberment Claim':'Others'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'Hospital And Surgical':'H&S'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'Hospital Cash Benefit':'HIB'}, inplace=True)
dfdata['CLAIM_TYPE'].replace({'TPDB Claim':'TPDB'}, inplace=True)
dfdata.groupby('CLAIM_TYPE').count()

# convert the CLAIM_STATUS_DATE, COMMENCEMENT_DATE and EVENT_DATE to datetime
dfdata['CLAIM_STATUS_DATE'] = pd.to_datetime(dfdata['CLAIM_STATUS_DATE'])
dfdata['COMMENCEMENT_DATE'] = pd.to_datetime(dfdata['COMMENCEMENT_DATE'])
dfdata['EVENT_DATE'] = pd.to_datetime(dfdata['EVENT_DATE'])

# add a column for CLAIM_YEAR
dfdata['CLAIM_STATUS_BY_YEAR'] = dfdata['CLAIM_STATUS_DATE'].dt.year
dfdata['CLAIM_STATUS_BY_YEAR'] = dfdata['CLAIM_STATUS_BY_YEAR'].astype(str).astype('object')

# add a column for POLICY_DURATION and calculate the duration of the policy
dfdata['POLICY_DURATION'] = dfdata['EVENT_DATE'].dt.year - dfdata['COMMENCEMENT_DATE'].dt.year

#dfdata['POLICY_DURATION'] = dfdata['POLICY_DURATION'].astype(str).astype('object')

dfdata['POLICY_DURATION'] = dfdata['POLICY_DURATION'].astype(str).astype(int)
# add new column to categorize policy duration
conditions = [
    (dfdata['POLICY_DURATION'] <= 1),
    (dfdata['POLICY_DURATION'] > 1) & (dfdata['POLICY_DURATION'] <= 5),
    (dfdata['POLICY_DURATION'] > 5)
    ]
values = ['0-1 year', '1-5 years', '>5 years']
dfdata['POL_DURATION'] = np.select(conditions, values)

#add new column to rename cause of event
dfdata['DIAGNOSIS'] = np.where(dfdata['CAUSE_OF_EVENT'] =='COVID-19','COVID-19', 'Others')

dfdata['DIAGNOSIS'].value_counts()

#checking on missing value
dfdata.isnull().sum()

# Commented out IPython magic to ensure Python compatibility.
#findings % of missing value
print('Percent of missing CAUSE_OF_EVENT record is %.f%% '
#        %((dfdata['CAUSE_OF_EVENT'].isnull().sum()/dfdata.shape[0]*100)))
print('Percent of missing LAST_DOC_RECEIVED record is %.f%% '
#        %((dfdata['LAST_DOC_RECEIVED'].isnull().sum()/dfdata.shape[0]*100)))
print('Percent of missing NET_PAYABLE_AMOUNT record is %.f%% '
#        %((dfdata['NET_PAYABLE_AMOUNT'].isnull().sum()/dfdata.shape[0]*100)))
print('Percent of missing NET_CLAIM_AMOUNT record is %.f%% '
#        %((dfdata['NET_CLAIM_AMOUNT'].isnull().sum()/dfdata.shape[0]*100)))

#impute the missing value
dfdata['CAUSE_OF_EVENT'].fillna(dfdata['CAUSE_OF_EVENT'].mode()[0],inplace = True)
dfdata['LAST_DOC_RECEIVED'].fillna(dfdata['LAST_DOC_RECEIVED'].mode()[0],inplace = True)
dfdata['NET_PAYABLE_AMOUNT'].fillna(dfdata['NET_PAYABLE_AMOUNT'].mode()[0],inplace = True)
dfdata['NET_CLAIM_AMOUNT'].fillna(dfdata['NET_CLAIM_AMOUNT'].mode()[0],inplace = True)
#checking missing value after impute the missing value
dfdata.isnull().sum()

#create new dataframe and to remove duplication by CLAIM_NO
dfdataclean = dfdata.drop_duplicates(subset=['CLAIM_NO'], keep='first')
dfdataclean.shape

dfdataclean.info()

dfdataclean.describe()

#dfdataclean
#outlier checker on clean data inclusive of all claims status = Approved, Reject, In Progress against the net payable amount
#Output is not significant to the result because claims status = Reject and In Progress does not have the accuracy of net payable amount
def OutlierChecker(dfdataclean):
  q1 = np.quantile(dfdataclean,0.25)
  q2 = np.quantile(dfdataclean,0.50)
  q3 = np.quantile(dfdataclean,0.75)
  IQR = q3 - q1
  Minimum = q1 - 1.5*IQR
  Maximum = q3 + 1.5*IQR
  Outlier = dfdataclean[(dfdataclean < Minimum) | (dfdataclean > Maximum)]
  return Outlier;

dfdataclean_sort = np.sort(dfdataclean['NET_PAYABLE_AMOUNT'])
median = np.median(dfdataclean['NET_PAYABLE_AMOUNT'])
q1 = np.quantile(dfdataclean_sort,0.25)
q2 = np.quantile(dfdataclean_sort,0.50)
q3 = np.quantile(dfdataclean_sort,0.75)
allQ = np.quantile(dfdataclean_sort,[0,0.25,0.5,0.75])
IQR = q3 - q1
Minimum = q1 - 1.5*IQR
Maximum = q3 + 1.5*IQR

print("Median = ",median)
print("Q1 = ",q1)
print("Q2 = ",q2)
print("Q3 = ",q3)
print("All quantile : ",allQ)
print("IQR = ",IQR)
print("Minimum = ",Minimum)
print("Maximum = ",Maximum)
print("How Many Outlier in Array? : " ,(dfdataclean_sort > Maximum).sum() + (dfdataclean_sort < Minimum).sum())
OutlierChecker(dfdataclean_sort)

#dfdataclean
import matplotlib.pyplot as plt
plt.figure(figsize = (6,6))   
ax = sb.countplot(data=dfdataclean, x='CLAIM_STATUS')
plt.xlabel("Claim Status")
plt.ylabel("No of Cases")
ax.set_title("No of Claims Processed for Y2018 - Y2022")
for label in ax.containers:
    ax.bar_label(label)

#dfdataclean
import matplotlib.pyplot as plt
ax = dfdataclean.groupby('CLAIM_STATUS').size()
sb.set()
ax.plot(kind='pie', title='No of Claims Processed for Y2018 - Y2022', figsize=[7,7],
          autopct=lambda p: '{:.2f}%\n({:.0f})'.format(p,(p/100)*ax.sum()), textprops = dict(color ="black"), label='')

#dfdataclean
import matplotlib.pyplot as plt
plt.figure(figsize = (20,5))  
ax = sb.countplot(data=dfdataclean, x='CLAIM_TYPE', hue='CLAIM_STATUS')
plt.xlabel("Claim Status")
plt.ylabel("No of Cases")
ax.set_title("No of Claims Processed for Y2018 - Y2022")
#ax.set_title("No of Cases Processed for Y2018 - Y202" + " according to Claim Status", bbox={'facecolor':'0.8', 'pad':3})
#plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

#dfdataclean
import matplotlib.pyplot as plt
plt.figure(figsize = (20,5))  
ax = sb.countplot(data=dfdataclean, x='CLAIM_TYPE')
plt.xlabel("Claim Type")
plt.ylabel("No of Cases")
ax.set_title("No of Claims Processed for Y2018 - Y2022")
#ax.set_title("No of Cases Processed for Y2018 - Y202" + " according to Claim Status", bbox={'facecolor':'0.8', 'pad':3})
#plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

#dfdataclean
import matplotlib.pyplot as plt
plt.figure(figsize = (15,5))  
data1 = dfdataclean.sort_values(by=['CLAIM_STATUS_BY_YEAR'])
ax = sb.countplot(data = data1, x='CLAIM_STATUS_BY_YEAR', hue='CLAIM_STATUS')
plt.xlabel("Year")
plt.ylabel("No of Cases")
ax.set_title("No of Claims Processed for Y2018 - Y2022")
#ax.set_title("No of Cases Processed for Y2018 - Y202" + " according to Claim Status", bbox={'facecolor':'0.8', 'pad':3})
#plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

#dfdataclean
import matplotlib.pyplot as plt
plt.figure(figsize = (15,5))  
data1 = dfdataclean.sort_values(by=['CLAIM_STATUS_BY_YEAR'])
ax = sb.countplot(data = data1, x='CLAIM_STATUS_BY_YEAR', hue='CLAIM_TYPE')
plt.xlabel("Year")
plt.ylabel("No of Cases")
ax.set_title("No of Claims Processed for Y2018 - Y2022")
#ax.set_title("No of Cases Processed for Y2018 - Y202" + " according to Claim Status", bbox={'facecolor':'0.8', 'pad':3})
#plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.legend(loc='upper center', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

#dfdataclean
import matplotlib.pyplot as plt
claims1 = dfdataclean.groupby('CLAIM_TYPE').size()
sb.set()
claims1.plot(kind='pie', title='No of Claim Processed for Y2018 - Y2022 according to Claim Type', figsize=[8,8],
          autopct=lambda p: '{:.2f}%\n({:.0f})'.format(p,(p/100)*claims1.sum()), label='')
plt.show()

#dfapproved
#copy data based on CLAIMS STATUS = APPROVED
dfapproved = dfdataclean[dfdataclean['CLAIM_STATUS'].str.contains("Approved")].copy()

dfapproved.info()

dfapproved.describe()

#outlier checker on claim status = approved to find outlier based on net payable amount
def OutlierChecker(dfapproved):
  Q1 = np.quantile(dfapproved,0.25)
  Q2 = np.quantile(dfapproved,0.50)
  Q3 = np.quantile(dfapproved,0.75)
  IQR = Q3-Q1
  Minimum = Q1 - 1.5*IQR
  Maximum = Q3 + 1.5*IQR
  Outlier = dfapproved[(dfapproved < Minimum) | (dfapproved > Maximum)]
  return Outlier;

dfapproved_sort = np.sort(dfapproved['NET_PAYABLE_AMOUNT'])
median = np.median(dfapproved['NET_PAYABLE_AMOUNT'])
Q1 = np.quantile(dfapproved_sort,0.25)
Q2 = np.quantile(dfapproved_sort,0.50)
Q3 = np.quantile(dfapproved_sort,0.75)
allQ = np.quantile(dfapproved_sort,[0,0.25,0.5,0.75])
IQR = Q3-Q1
Minimum = Q1 - 1.5*IQR
Maximum = Q3 + 1.5*IQR

print("Median = ",median)
print("Q1 = ",Q1)
print("Q2 = ",Q2)
print("Q3 = ",Q3)
print("All quantile : ",allQ)
print("IQR = ",IQR)
print("Minimum = ",Minimum)
print("Maximum = ",Maximum)
print("How Many Outlier in Array? : " ,(dfapproved_sort > Maximum).sum() + (dfapproved_sort < Minimum).sum())
OutlierChecker(dfapproved_sort)

#dfapproved
#ax = sb.countplot(data=dfapproved, x='CLAIM_STATUS_BY_YEAR', hue='CLAIM_STATUS')
ax = sb.countplot(data=dfapproved, x='CLAIM_STATUS_BY_YEAR')
plt.xlabel("Year")
plt.ylabel("No of Cases")
ax.set_title("No of Claims Approved for Y2018 - Y2022")
for label in ax.containers:
    ax.bar_label(label)
#ax.legend(loc='upper left',
#          fancybox=True, shadow=True, ncol=5)

#dfapproved
import matplotlib.pyplot as plt
claims = dfapproved.groupby('CLAIM_TYPE').size()

sb.set()
claims.plot(kind='pie', title='No of Cases Approved for Y2018 - Y2022 according to Claim Type', figsize=[10,10],
          autopct=lambda p: '{:.2f}%({:.0f})'.format(p,(p/100)*claims.sum()), label='')
plt.show()

#dfapproved
plt.figure(figsize = (10,8))  
ax = sb.countplot(data=dfapproved, y='CLAIM_TYPE', hue='CLAIM_STATUS_BY_YEAR')
plt.xlabel("Year")
plt.ylabel("No of Cases")
ax.set_title("No of Claims Approved for Y2018 - Y2022 according to Claim Type")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

#RUN LAST AS IT TAKING TIME
g = sb.PairGrid(dfapproved, hue="CLAIM_TYPE")
g.map_diag(sb.histplot)
g.map_offdiag(sb.scatterplot)
g.add_legend()

# Import libraries
import numpy as np
import matplotlib.pyplot as plt

# Creating dataset
claim = ['Death','Critical Illness','Funeral Expenses','H&S','HIB','Others','TPDB']
data = [23035, 647, 12020, 88, 7798, 875, 1480]

# Creating explode data
explode = (0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 0.0)

# Creating color parameters
colors = ( "orange", "cyan", "violet",	"grey", "gold", "lightcoral","pink")

# Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "darkblue" }

# Creating autocpt arguments
def func(pct, allvalues):
	absolute = int(pct / 100.*np.sum(allvalues))
	return "{:.1f}%".format(pct, absolute)

# Creating plot
fig, ax = plt.subplots(figsize =(8, 8))
wedges, texts, autotexts = ax.pie(data,
								autopct = lambda pct: func(pct, data),
								explode = explode,
								labels = claim,
								shadow = False,
								colors = colors,
								startangle = 90,
								wedgeprops = wp,
								textprops = dict(color ="blue"))
# Adding legend
#ax.legend(wedges, claim,
#		title ="Claim Type",
#		loc ="center left",
#		bbox_to_anchor =(1, 0, 0.5, 1))

#plt.setp(autotexts, size = 10, weight ="bold")
plt.setp(autotexts, size = 12)
ax.set_title("No of Claims Approved for Y2018 - Y2022 according to Claim Type")

# show plot
plt.show()

plt.figure(figsize = (10,5))   
data3 = dfdataclean.sort_values(by=['CLAIM_STATUS_BY_YEAR'])
ax = sb.countplot(data=data3, x='CLAIM_STATUS_BY_YEAR', hue='DIAGNOSIS')
plt.xlabel("Year")
plt.ylabel("No of Cases")
ax.set_title("No of Claims Processed for Y2018 - Y2022 according to Covid-19")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

plt.figure(figsize = (8,5))   
ax = sb.countplot(data=dfdataclean, x='POL_DURATION')
plt.xlabel("Policy Duration")
plt.ylabel("No of Cases")
ax.set_title("No of Death Claims Approved for Y2018 - Y2022 according to Policy Duration")
#plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

plt.figure(figsize = (20,5))   
ax = sb.countplot(data=dfdataclean, x='POL_DURATION', hue='CLAIM_STATUS_BY_YEAR')
plt.xlabel("Policy Duration")
plt.ylabel("No of Cases")
ax.set_title("No of Death Claims Approved for Y2018 - Y2022 according to Policy Duration")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

dfdeath = dfapproved[dfapproved['CLAIM_TYPE'].str.contains("Death")].copy()
dfdeath.shape

import matplotlib.pyplot as plt
plt.figure(figsize = (15,5))  
data2 = dfdeath.sort_values(by=['CLAIM_STATUS_BY_YEAR'])
ax = sb.countplot(data = data2, x='CLAIM_STATUS_BY_YEAR', hue='POL_DURATION')
plt.xlabel("Year")
plt.ylabel("No of Cases")
ax.set_title("No of Death Claims Approved for Y2018 - Y2022 according to Policy Duration")
plt.legend(loc='upper center', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

import matplotlib.pyplot as plt
claims = dfdeath.groupby('POL_DURATION').size()

sb.set()
claims.plot(kind='pie', title='No of Death Claims Approved for Y2018 - Y2022 according to Policy Duration', figsize=[5,5],
          autopct=lambda p: '{:.2f}%({:.0f})'.format(p,(p/100)*claims.sum()), label='')
plt.show()

#outlier checker on death claim approved to find outlier based on net payable amount
def OutlierChecker(dfdeath):
  Q1 = np.quantile(dfdeath,0.25)
  Q2 = np.quantile(dfdeath,0.50)
  Q3 = np.quantile(dfdeath,0.75)
  IQR = Q3-Q1
  Minimum = Q1 - 1.5*IQR
  Maximum = Q3 + 1.5*IQR
  Outlier = dfdeath[(dfdeath < Minimum) | (dfdeath > Maximum)]
  return Outlier;

dfdeath_sort = np.sort(dfdeath['NET_PAYABLE_AMOUNT'])
median = np.median(dfdeath['NET_PAYABLE_AMOUNT'])
Q1 = np.quantile(dfdeath_sort,0.25)
Q2 = np.quantile(dfdeath_sort,0.50)
Q3 = np.quantile(dfdeath_sort,0.75)
allQ = np.quantile(dfdeath_sort,[0,0.25,0.5,0.75])
IQR = Q3-Q1
Minimum = Q1 - 1.5*IQR
Maximum = Q3 + 1.5*IQR

print("Median = ",median)
print("Q1 = ",Q1)
print("Q2 = ",Q2)
print("Q3 = ",Q3)
print("All quantile : ",allQ)
print("IQR = ",IQR)
print("Minimum = ",Minimum)
print("Maximum = ",Maximum)
print("How Many Outlier in Array? : " ,(dfdeath_sort > Maximum).sum() + (dfdeath_sort < Minimum).sum())
OutlierChecker(dfdeath_sort)

import matplotlib.pyplot as plt
claims = dfdeath.groupby('DIAGNOSIS').size()

sb.set()
claims.plot(kind='pie', title='No of Death Claims Approved for Y2018 - Y2022 according to Diagnosis', figsize=[5,5],
          autopct=lambda p: '{:.2f}%({:.0f})'.format(p,(p/100)*claims.sum()), label='')
plt.show()

plt.figure(figsize = (5,5))   
ax = sb.countplot(data=dfdeath, x='DIAGNOSIS')
plt.xlabel("Policy Duration")
plt.ylabel("Diagnosis")
ax.set_title("No of Death Claims Approved for Y2018 - Y2022 according to Diagnosis")
#plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

plt.figure(figsize = (10,5))   
data3 = dfdeath.sort_values(by=['CLAIM_STATUS_BY_YEAR'])
ax = sb.countplot(data=data3, x='CLAIM_STATUS_BY_YEAR', hue='DIAGNOSIS')
plt.xlabel("Year")
plt.ylabel("No of Cases")
ax.set_title("No of Death Claims Approved for Y2018 - Y2022 according to Diagnosis")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
for label in ax.containers:
    ax.bar_label(label)

SelectedColumns=['CLAIM_NO','CLAIM_TYPE','POL_DURATION','NET_PAYABLE_AMOUNT','DIAGNOSIS','CLAIM_STATUS_BY_YEAR','CLAIM_STATUS','POLICY_DURATION']
DataMax=dfdataclean[SelectedColumns]
DataMax[DataMax['NET_PAYABLE_AMOUNT'] == DataMax['NET_PAYABLE_AMOUNT'].max()]

!pip install sweetviz

# importing sweetviz library
import sweetviz as sv

#analyzing the dataset
advert_report = sv.analyze(dfapproved)

#display the report
advert_report.show_html('NAA_Claims.html')
advert_report.show_notebook()

"""**Supervised with Gaussian Naive Bayes**"""

SelectedColumns=['POL_DURATION','NET_PAYABLE_AMOUNT','DIAGNOSIS','CLAIM_STATUS_BY_YEAR','CLAIM_STATUS']
# Selecting final columns
DataForML=dfdataclean[SelectedColumns]
DataForML.head()

#Saving this final data for reference during deployment
DataForML.to_pickle('DataForML.pkl')

# Treating the binary nominal variables first
DataForML['DIAGNOSIS'].replace({'COVID-19':0,'Others':1}, inplace=True)
DataForML['CLAIM_STATUS_BY_YEAR'].replace({'2018':0,'2019':1,'2020':3,'2021':4, '2022':5},inplace=True)
DataForML['POL_DURATION'].replace({'0-1 year':0,'1-5 years':1,'>5 years':3},inplace=True)
DataForML['CLAIM_STATUS'].replace({'Approved':0,'In Progress':1,'Rejected':2},inplace=True)

# Looking at data after nominal treatment
DataForML.head()

# Treating all the nominal variables at once using dummy variables
DataForML_Numeric=pd.get_dummies(DataForML)

# Adding Target Variable to the data
DataForML_Numeric['CLAIM_STATUS']=dfdataclean['CLAIM_STATUS']

# Printing sample rows
DataForML_Numeric.head()

# Printing all the column names for our reference
DataForML_Numeric.columns

# Separate Target Variable and Predictor Variables
TargetVariable = ['DIAGNOSIS']
Predictors=['POL_DURATION', 'NET_PAYABLE_AMOUNT', 'DIAGNOSIS','CLAIM_STATUS_BY_YEAR']      

X=DataForML_Numeric[Predictors].values
y=DataForML_Numeric[TargetVariable].values

# Split the data into training and testing set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3,random_state=1000)

# Sanity check for the sampled data
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

from sklearn.naive_bayes import GaussianNB # 1. choose model class
model = GaussianNB()                       # 2. instantiate model
model.fit(X_train,y_train)                # 3. fit model to data

from sklearn.naive_bayes import GaussianNB # 1. choose model class
model = GaussianNB()                       # 2. instantiate model
model.fit(X_train,y_train)                # 3. fit model to data
y_model = model.predict(X_test)            # 4. predict on new data

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_model)

from sklearn.metrics import classification_report

print(classification_report(y_test, y_model))

# Confusion Matrix
from sklearn.metrics import confusion_matrix 
confusion_matrix(y_test, y_model)

#Confusion Matrix
import matplotlib.pyplot as plt
from sklearn import metrics
import numpy as np
confusion_matrix = metrics.confusion_matrix(y_test, y_model)

print(confusion_matrix)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix,display_labels=np.unique(y))
cm_display.plot()
plt.show()

from sklearn.metrics import classification_report
# F1 score = 2 / [ (1/precision) + (1/ recall)]
print(classification_report(y_test, y_model))

"""**Unsupervised - Principal Component Analysis**"""

#Principal Component Analysis
SelectedColumns=['POL_DURATION','NET_PAYABLE_AMOUNT','DIAGNOSIS','CLAIM_STATUS_BY_YEAR','CLAIM_STATUS']
Datapca=dfdataclean[SelectedColumns]

Datapca['DIAGNOSIS'].replace({'COVID-19':0,'Others':1}, inplace=True)
Datapca['CLAIM_STATUS_BY_YEAR'].replace({'2018':0,'2019':1,'2020':3,'2021':4, '2022':5},inplace=True)
Datapca['POL_DURATION'].replace({'0-1 year':0,'1-5 years':1,'>5 years':3},inplace=True)
Datapca['CLAIM_STATUS'].replace({'Approved':0,'In Progress':1,'Rejected':2},inplace=True)

X = Datapca.drop(['DIAGNOSIS'], axis=1)
y = Datapca['DIAGNOSIS']

print(X.shape, y.shape)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.decomposition import PCA

pca = PCA().fit(X_train)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance');

accum_explained_var = np.cumsum(pca.explained_variance_ratio_)

min_threshold = np.argmax(accum_explained_var > 0.90) # use 90%

min_threshold

pca = PCA(n_components = min_threshold + 1)

X_train_projected= pca.fit_transform(X_train)
X_test_projected = pca.transform(X_test)

X_train_projected.shape

#Logistic Regression Classification without PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report

logregwithoutpca = LogisticRegression()
logregwithoutpca.fit(X_train, y_train)

logregwithoutpca_result = logregwithoutpca.predict(X_test)

print('Accuracy of Logistic Regression (without PCA) on training set: {:.2f}'
     .format(logregwithoutpca.score(X_train, y_train)))
print('Accuracy of Logistic Regression (without PCA)  on testing set: {:.2f}'
     .format(logregwithoutpca.score(X_test, y_test)))
print('\nConfusion matrix :\n',confusion_matrix(y_test, logregwithoutpca_result))
print('\n\nClassification report :\n\n', classification_report(y_test, logregwithoutpca_result))

#Logistic Regression Classification with PCA
logregwithpca = LogisticRegression()
logregwithpca.fit(X_train_projected, y_train)

logregwithpca_result = logregwithpca.predict(X_test_projected)

print('Accuracy of Logistic Regression (with PCA) on training set: {:.2f}'
     .format(logregwithpca.score(X_train_projected, y_train)))
print('Accuracy of Logistic Regression (with PCA) on testing set: {:.2f}'
     .format(logregwithpca.score(X_test_projected, y_test)))
print('\nConfusion matrix :\n',confusion_matrix(y_test, logregwithpca_result))
print('\n\nClassification report :\n\n', classification_report(y_test, logregwithpca_result))