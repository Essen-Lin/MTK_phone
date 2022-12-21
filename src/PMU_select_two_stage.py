from scipy.cluster.hierarchy import dendrogram, linkage,fcluster,leaves_list,cut_tree,DisjointSet
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score 
import statsmodels.api  as  sm
import csv

# Read each CSV file in dir "path/to/root_dir"
directory = "/Users/essen/Desktop/MTK_experiment/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/benchmark_data/pixel4XL/Mi_Lm"
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

def generate_pmu_data(cluster,frequency,task):
  data = []
  pmu_num = 150
  row_num = (cluster*3+frequency)*pmu_num
  for i in range(150):
    data.append(task['count'][row_num+i].replace(',',''))
  return data

def generate_pmu_r(cluster):
  average_r =[]
  total = [0]*PMU_num
  for i in range(PMU_num):
    for frequency in range(3):
        data = generate_PMU_R(cluster,frequency)
        total[i] = total[i]+data[i]
    average_r.append(total[i]/3)
  return average_r

def generate_pmu_average_count(cluster):
  count = []*PMU_num
  total = [0]*PMU_num
  for i in range(PMU_num):
    for frequency in range(3):
      for t in dfs:
        data = generate_pmu_data(cluster,frequency,t)
        total[i] = total[i]+int(data[i])
    count.append(total[i]/(3*len(dfs)))
  return count

def draw_cluster_by_CPU_Cluster(cluster):
  PMU_avg = generate_pmu_average_count(cluster)
  X = [[i] for i in PMU_avg]
  HCA = linkage(X,metric='euclidean',method='single')
  PMU_cluster_list = leaves_list(HCA)
  # fig = plt.figure(figsize=(30, 20))
  # dn = dendrogram(HCA)
  # plt.show()
  # print(PMU_cluster_list)
  return PMU_cluster_list

def draw_cluster_r(cluster,r_limit):
  selection_list=[]
  selection_list_r =[]
  PMU_cluster_list = draw_cluster_by_CPU_Cluster(cluster)
  pmu_x = [PMU_list[i] for i in PMU_cluster_list]
  r_value = generate_pmu_r(0)
  pmu_y = [r_value[i]for i in PMU_cluster_list]
  # print(pmu_x)
  # print(pmu_y)
  # fig = plt.figure(figsize=(30, 20))
  # plt.xticks(rotation=90)
  # plt.bar(pmu_x,pmu_y)
  # plt.show()
  for i in range(len(pmu_y)):
    if pmu_y[i] > r_limit:
      selection_list.append(pmu_x[i])
      selection_list_r.append(pmu_y[i])
  
  return selection_list

# #利用Cluster leaf 的順序做長條圖
# #根據論文中提到的演算法來篩選PMU

def train_dataset(cluster,selection_list):
  train_data ={}
  idx = cluster*len(PMU_list)
  
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
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0)

  regressor = LinearRegression()
  model=regressor.fit(X_train, y_train)

  return model.score(X, y)

def pmu_selection_r_squared(cluster,selection_list):
  pmu_list = ["raw-cpu-cycles"]
  result = ["raw-cpu-cycles"]
  best_r = train_model(cluster,pmu_list)

  for i in (selection_list):
    pmu_list.append(i)
    pmu_list = list(dict.fromkeys(pmu_list))
    new_R = train_model(cluster,pmu_list)
    if new_R > best_r:
      result.append(i)
      best_r = new_R
    else:
      pmu_list.remove(i)
  if len(result) > 6:
    return result[0:7]
  else:
    return result
  
def final_model(cluster,selection_list):
  data = train_dataset(cluster,selection_list)

  y = data.iloc[:, len(selection_list)]
  X = data.iloc[:, 0:len(selection_list)]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

  regressor = LinearRegression()
  model=regressor.fit(X_train, y_train)
  y_predict = regressor.predict(X_test)
  score1=r2_score(y_test,y_predict)

  diff_ratio = 0
  y_test = list(y_test)
  for i in range(len(y_predict)):
    diff_ratio = diff_ratio + abs((y_predict[i]-y_test[i])/y_test[i])
    print("predict time:", y_predict[i],"real time:", y_test[i])
  diff_ratio = 100* diff_ratio / len(y_predict)

  Validation_R=r2_score(y_test,y_predict)

  # print("model.intercept_:",model.intercept_)
  # print("model.coef_:",model.coef_)

  # print("R:",model.score(X, y))
  # print("Validation R: ",score1)
  # print("Different Ration: ",diff_ratio*100,"%")
  return Validation_R, diff_ratio

def print_train_model():
  R_value = 0.75
  CPU = []

  # for cluster in range(cluster_num):
  #   # CPU.append(dfs[0]['setup core'][PMU_num*cluster_num*cluster])
  #   PMU_selection = pmu_selection_r_squared(cluster,draw_cluster_r(cluster,R_value))
  #   print('CPU:',dfs[0]['setup core'][PMU_num*frequency_num*cluster],'PMU_list:',PMU_selection)
  #   final_model(cluster,PMU_selection)

  with open('/Users/essen/Desktop/MTK_experiment/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/result/two_stage/two_stage_pmu.csv', 'w', newline='') as csvfile:
  # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    # 寫入一列資料
    writer.writerow(['Cluster (CPU)', 'PMU 1', 'PMU2','PMU 3','PMU 4','PMU 5','PMU 6','PMU 7','Validation R','Different Ratio'])

    for cluster in range(cluster_num):
      CPU.append(dfs[0]['setup core'][PMU_num*frequency_num*cluster])
      PMU_selection = pmu_selection_r_squared(cluster,draw_cluster_r(cluster,R_value))
      print('CPU:',dfs[0]['setup core'][PMU_num*frequency_num*cluster],'PMU_list:',PMU_selection)
      row = [' ']*10
      row[0] = (dfs[0]['setup core'][PMU_num*frequency_num*cluster])
      row[1:1+len(PMU_selection)] = PMU_selection

      Validation_R, diff_ratio= final_model(cluster,PMU_selection)
      print('R: ',Validation_R,"Different Ratio: ",diff_ratio,"%")
      row[8] = Validation_R
      row[9] = str(diff_ratio)+'%'
      writer.writerow(row)


def main():
  print_train_model()

if __name__ == "__main__":
    main()
