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
# big = generate_PMU_R(1,PMU_list)
# prime = generate_PMU_R(2,PMU_list)

# def PMU_selection_by_all_freq(cluster_r,r_value,PMU_list):
#   PMU_select =[]
#   for i in range(len(PMU_list)):
#     if abs(cluster_r[i]) >= r_value:
#       PMU_select.append(PMU_list[i])

#   return PMU_select