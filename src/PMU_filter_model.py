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

