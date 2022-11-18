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

def generate_PMU_R (cluster):
    PMU_R = []
    for i in range(PMU_num):
      count = []
      time = []
      for j in range(frequency_num):
        pmu_c = (cluster*frequency_num+j)*PMU_num
        count = count + (list)(convert_float(df['count'][i + pmu_c]))
        time = time + (list)(df['time'][i + pmu_c])
      PMU_R.append(r(count,time))
    return PMU_R


def PMU_selection_by_all_freq(cluster_r,r_value):
  PMU_select =[]
  for i in range(len(PMU_list)):
    if abs(cluster_r[i]) >= r_value:
      PMU_select.append(PMU_list[i])

  return PMU_select


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


def train_model(cluster,R_value):
  selection_list = PMU_selection_by_all_freq(generate_PMU_R(cluster),R_value)
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
    CPU.append(dfs[0]['setup core'][PMU_num*cluster_num*i])
    PMU_selection = PMU_selection_by_all_freq(generate_PMU_R(i),R_value)
    print('CPU:',dfs[0]['setup core'][PMU_num*cluster_num*i],'PMU_list:',PMU_selection)
    train_model(i,R_value)

def main():
  print_train_model()

if __name__ == "__main__":
    main()