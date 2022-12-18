import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score 

# Read each CSV file in dir "path/to/root_dir"
directory = "../benchmark_data"
dfs = []

for file in Path(directory).glob("**/*.csv"):
    dfs.append(pd.read_csv(file))
# Put the dataframes to a single dataframe
df = pd.concat(dfs)

PMU_list = dfs[0]['event'][0:150]
PMU_num = len(PMU_list)
frequency_num = 3
cluster_num = (int)((len(dfs[0])/frequency_num)/PMU_num)

def countPerSec(df):
  countPerSec = []
  for count,time in zip(list((df['count'])), list((df['time']))):
    countPerSec.append(int(count.replace(',',''))/time)
  return np.array(countPerSec)

def percentage_variation(VAL1,AVL2):
  return abs(VAL1-AVL2) / ((VAL1+AVL2)/2) * 100


#Filter 1
# little
countPerSec_300000 = countPerSec(dfs[0][(dfs[0]['frequency']==300000)])
countPerSec_1036800 = countPerSec(dfs[0][(dfs[0]['frequency']==1036800)])
countPerSec_1785600 = countPerSec(dfs[0][(dfs[0]['frequency']==1785600)])

avg_little = (countPerSec_300000 + countPerSec_1036800 + countPerSec_1785600) / 3

percentage_variation_300000 = percentage_variation(avg_little,countPerSec_300000)
percentage_variation_1036800 = percentage_variation(avg_little,countPerSec_1036800)
percentage_variation_1785600 = percentage_variation(avg_little,countPerSec_1785600)

sum_little = (percentage_variation_300000 + percentage_variation_1036800 + percentage_variation_1785600)

i = 0
filterEvent_little = []
for x in sum_little:
  if x > 10 and ~np.isnan(x):
    filterEvent_little.append(dfs[0][:150]['event'][i])
  i = i+1

# middle
countPerSec_710400 = countPerSec(dfs[0][(dfs[0]['frequency']==710400)])
countPerSec_1612800 = countPerSec(dfs[0][(dfs[0]['frequency']==1612800)])
countPerSec_2419200 = countPerSec(dfs[0][(dfs[0]['frequency']==2419200)])

avg_middle = (countPerSec_710400 + countPerSec_1612800 + countPerSec_2419200) / 3

percentage_variation_710400 = percentage_variation(avg_middle,countPerSec_710400)
percentage_variation_1612800 = percentage_variation(avg_middle,countPerSec_1612800)
percentage_variation_2419200 = percentage_variation(avg_middle,countPerSec_2419200)

sum_middle = (percentage_variation_710400 + percentage_variation_1612800 + percentage_variation_2419200)

i = 0
filterEvent_middle = []
for x in sum_middle:
  if x > 10 and ~np.isnan(x):
    filterEvent_middle.append(dfs[0][:150]['event'][i])
  i = i+1

# big
countPerSec_825600 = countPerSec(dfs[0][(dfs[0]['frequency']==825600)])
countPerSec_1804800 = countPerSec(dfs[0][(dfs[0]['frequency']==1804800)])
countPerSec_2841600 = countPerSec(dfs[0][(dfs[0]['frequency']==2841600)])

avg_big = (countPerSec_825600 + countPerSec_1804800 + countPerSec_2841600) / 3

percentage_variation_825600 = percentage_variation(avg_big,countPerSec_825600)
percentage_variation_1804800 = percentage_variation(avg_big,countPerSec_1804800)
percentage_variation_2841600 = percentage_variation(avg_big,countPerSec_2841600)

sum_big = (percentage_variation_825600 + percentage_variation_1804800 + percentage_variation_2841600)

i = 0
filterEvent_big = []
for x in sum_big:
  if x > 10 and ~np.isnan(x):
    filterEvent_big.append(dfs[0][:150]['event'][i])
  i = i+1

#print(df1[df1['event'].isin(filterEvent)])
#被過濾掉的
#print(df1[~df1.event.isin(filterEvent)])

# print("filterEvent_little [%d]: %s "%(len(filterEvent_little), filterEvent_little.__str__()))
# print("filterEvent_middle [%d]: %s "%(len(filterEvent_middle), filterEvent_middle.__str__()))
# print("filterEvent_big : [%d]: %s "%(len(filterEvent_big), filterEvent_big.__str__()))

#Filter 2
def counts(df):
  counts = []
  for count in list((df['count'])):
    counts.append(int(count.replace(',','')))
  return np.array(counts)

df_little = dfs[0][:150][dfs[0][:150]['event'].isin(filterEvent_little)]
df_middle = dfs[0][:150][dfs[0][:150]['event'].isin(filterEvent_middle)]
df_big = dfs[0][:150][dfs[0][:150]['event'].isin(filterEvent_big)]

# little
df_little_300000 = dfs[0][(dfs[0]['frequency']==300000)]
df_little_300000 = df_little_300000[df_little_300000['event'].isin(filterEvent_little)]
counts_300000 = counts(df_little_300000)
#print(df_little_300000)

df_little_1036800 = dfs[0][(dfs[0]['frequency']==1036800)]
df_little_1036800 = df_little_1036800[df_little_1036800['event'].isin(filterEvent_little)]
counts_1036800 = counts(df_little_1036800)
#print(df_little_1036800)

df_little_1785600 = dfs[0][(dfs[0]['frequency']==1785600)]
df_little_1785600 = df_little_1785600[df_little_1785600['event'].isin(filterEvent_little)]
counts_1785600 = counts(df_little_1785600)
#print(df_little_1785600)

avg_little = (counts_300000 + counts_1036800 + counts_1785600)/3

percentage_variation_300000 = percentage_variation(avg_little,counts_300000)
percentage_variation_1036800 = percentage_variation(avg_little,counts_1036800)
percentage_variation_1785600 = percentage_variation(avg_little,counts_1785600)

sum_little = (percentage_variation_300000 + percentage_variation_1036800 + percentage_variation_1785600)
#print(sum_little)
rankingOfEvents = np.argsort(sum_little)[::-1]
#print(rankingOfEvents)

# print(df_little)
# print(df_little.iloc[rankingOfEvents[0]]['event'])

filterEvent_little = []
for i in rankingOfEvents:
  filterEvent_little.append(df_little.iloc[i]['event'])
# print(filterEvent_little)

# middle
df_middle_710400 = dfs[0][(dfs[0]['frequency']==710400)]
df_middle_710400 = df_middle_710400[df_middle_710400['event'].isin(filterEvent_middle)]
counts_710400 = counts(df_middle_710400)
#print(df_middle_710400)

df_middle_1612800 = dfs[0][(dfs[0]['frequency']==1612800)]
df_middle_1612800 = df_middle_1612800[df_middle_1612800['event'].isin(filterEvent_middle)]
counts_1612800 = counts(df_middle_1612800)
#print(df_middle_1612800)

df_middle_2419200 = dfs[0][(dfs[0]['frequency']==2419200)]
df_middle_2419200 = df_middle_2419200[df_middle_2419200['event'].isin(filterEvent_middle)]
counts_2419200 = counts(df_middle_2419200)
#print(df_middle_2419200)

avg_middle = (counts_710400 + counts_1612800 + counts_2419200)/3

percentage_variation_710400 = percentage_variation(avg_middle,counts_710400)
percentage_variation_1612800 = percentage_variation(avg_middle,counts_1612800)
percentage_variation_2419200 = percentage_variation(avg_middle,counts_2419200)

sum_middle = (percentage_variation_710400 + percentage_variation_1612800 + percentage_variation_2419200)
#print(sum_middle)
rankingOfEvents = np.argsort(sum_middle)[::-1]
#print(rankingOfEvents)

filterEvent_middle = []
for i in rankingOfEvents:
  filterEvent_middle.append(df_middle.iloc[i]['event'])
#print(filterEvent_middle)

# big
df_big_825600 = dfs[0][(dfs[0]['frequency']==825600)]
df_big_825600 = df_big_825600[df_big_825600['event'].isin(filterEvent_big)]
counts_825600 = counts(df_big_825600)
#print(df_big_825600)

df_big_1804800 = dfs[0][(dfs[0]['frequency']==1804800)]
df_big_1804800 = df_big_1804800[df_big_1804800['event'].isin(filterEvent_big)]
counts_1804800 = counts(df_big_1804800)
#print(df_big_1804800)

df_big_2841600 = dfs[0][(dfs[0]['frequency']==2841600)]
df_big_2841600 = df_big_2841600[df_big_2841600['event'].isin(filterEvent_big)]
counts_2841600 = counts(df_big_2841600)
#print(df_big_2841600)

avg_big = (counts_825600 + counts_1804800 + counts_2841600)/3

percentage_variation_825600 = percentage_variation(avg_big,counts_825600)
percentage_variation_1804800 = percentage_variation(avg_big,counts_1804800)
percentage_variation_2841600 = percentage_variation(avg_big,counts_2841600)

sum_big = (percentage_variation_825600 + percentage_variation_1804800 + percentage_variation_2841600)
#print(sum_big)
rankingOfEvents = np.argsort(sum_big)[::-1]
#print(rankingOfEvents)

filterEvent_big = []
for i in rankingOfEvents:
  filterEvent_big.append(df_big.iloc[i]['event'])
#print(filterEvent_big)

print(filterEvent_little[:6])
print(filterEvent_middle[:6])
print(filterEvent_big[:6])


def train_dataset(cluster,selection_list):
  train_data ={}
  idx = cluster*PMU_num
  
  for pmu in selection_list:
    count = []
    for t in dfs:
      for frequency in range(frequency_num):
          count.append(t['count'][list(PMU_list).index(pmu)+idx+frequency*len(PMU_list)].replace(',',''))
    train_data[pmu] = np.array(count)
  time = []
  for t in dfs:
    for frequency in range(frequency_num):
      time.append( t['time'][idx+frequency*len(PMU_list)])
  train_data['time'] = np.array(time)
  return  pd.DataFrame(train_data)


def train_model(cluster,selection_list):
  data = train_dataset(cluster,selection_list)

  y = data.iloc[:, len(selection_list)]
  X = data.iloc[:, 0:len(selection_list)]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

  regressor = LinearRegression()
  model=regressor.fit(X_train, y_train)

  y_predict = regressor.predict(X_test)
  score1=r2_score(y_test,y_predict)

  diff_ratio = 0
  y_test = list(y_test)
  for i in range(len(y_predict)):
    diff_ratio = diff_ratio + ((y_predict[i]-y_test[i])/y_test[i])
  diff_ratio = diff_ratio / len(y_predict)

  score1=r2_score(y_test,y_predict)

  print("model.intercept_:",model.intercept_)
  print("model.coef_:",model.coef_)

  print("R:",model.score(X, y))
  print("Validation R: ",score1)
  print("Different Ration: ",diff_ratio,"%")


def print_train_model():
  R_value = 0.9
  CPU = []

  for i in range(cluster_num):
    CPU.append(dfs[0]['setup core'][PMU_num*frequency_num*i])
    PMU_selection = PMU_selection_by_all_freq(generate_PMU_R(i),R_value)
    print('CPU:',dfs[0]['setup core'][PMU_num*frequency_num*i],'PMU_list:',PMU_selection)
    train_model(i,R_value)

def main():
  print_train_model()

if __name__ == "__main__":
    main()