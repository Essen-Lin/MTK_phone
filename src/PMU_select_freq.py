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

def convert_float(num):
  b = [float(i.replace(",","")) for i in num]
  return b

def r(x, y):
    x = np.array(x)
    y = np.array(y)
    xm = x.mean()
    ym = y.mean()
    numerator = np.sum(((x - xm) * (y - ym)))
    denominator = np.sqrt(np.sum((x - xm) ** 2)) * np.sqrt(np.sum((y - ym) ** 2))
    if denominator == 0 :
        return 0
    else:
        return numerator / denominator 

def generate_PMU_R (cluster,frequency):
    PMU_R = []
    pmu_c = (cluster*frequency_num+frequency)*PMU_num

    for i in range(PMU_num):
      count = (convert_float(df['count'][i + pmu_c]))
      time = (df['time'][i + pmu_c])
      PMU_R.append(r(count,time))
    return PMU_R

def PMU_selection_by_each_freq(cluster_r,r_value):
  PMU_select =[]
  for i in range(len(PMU_list)):
    if abs(cluster_r[i]) >= r_value:
      PMU_select.append(PMU_list[i])

  return PMU_select

def print_PMU_by_each_freq():
  R_value = 0.99
  CPU = []
  frequency = []
  PMU_selection = []
  for i in range(cluster_num):
    for j in range(frequency_num):
      CPU.append(dfs[0]['setup core'][PMU_num*cluster_num*i])
      frequency.append(dfs[0]['frequency'][PMU_num*j])
      print('CPU:',dfs[0]['setup core'][PMU_num*cluster_num*i],'Frequency:',dfs[0]['frequency'][PMU_num*j])
      print('PMU list: ',PMU_list)
      PMU_selection = PMU_selection+PMU_selection_by_each_freq(generate_PMU_R(i,j),R_value)
  result = list(dict.fromkeys(PMU_selection))
  return result


def train_dataset(cluster,frequency,selection_list):
  train_data ={}
  idx = cluster*PMU_num
  
  for pmu in selection_list:
    count = []
    for t in dfs:
      count.append(t['count'][list(PMU_list).index(pmu)+idx+frequency*len(PMU_list)].replace(',',''))
    train_data[pmu] = np.array(count)
  time = []
  for t in dfs:
    time.append( t['time'][idx+frequency*len(PMU_list)])
  train_data['time'] = np.array(time)
  return  pd.DataFrame(train_data)


def train_model(cluster,frequency,R_value):
  selection_list = PMU_selection_by_each_freq(generate_PMU_R(cluster,frequency),R_value)
  data = train_dataset(cluster,frequency,selection_list)

  y = data.iloc[:, len(selection_list)]
  X = data.iloc[:, 0:len(selection_list)]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0)

  regressor = LinearRegression()
  model=regressor.fit(X_train, y_train)

  y_predict = regressor.predict(X_test)
  score1=r2_score(y_test,y_predict)

  print("model.intercept_:",model.intercept_)
  print("model.coef_:",model.coef_)

  print("R:",model.score(X, y))
  print("Validation R: ",score1)
  


def print_train_model():
  R_value = 0.99
  CPU = []
  frequency = []

  for i in range(cluster_num):
    for j in range(frequency_num):
      CPU.append(dfs[0]['setup core'][PMU_num*frequency_num*i])
      frequency.append(dfs[0]['frequency'][PMU_num*j])
      PMU_selection = PMU_selection_by_each_freq(generate_PMU_R(i,j),R_value)
      print('CPU:',dfs[0]['setup core'][PMU_num*frequency_num*i],'Frequency:',dfs[0]['frequency'][PMU_num*j],'PMU_list:',PMU_selection)
      train_model(i,j,R_value)



def main():
  print_train_model()

if __name__ == "__main__":
    main()