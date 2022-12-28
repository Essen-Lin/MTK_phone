## MTK 產學合作計畫 

<!-- TOC -->

- [MTK 產學合作計畫](#mtk-%E7%94%A2%E5%AD%B8%E5%90%88%E4%BD%9C%E8%A8%88%E7%95%AB)
    - [計畫目標](#%E8%A8%88%E7%95%AB%E7%9B%AE%E6%A8%99)
    - [設備規格](#%E8%A8%AD%E5%82%99%E8%A6%8F%E6%A0%BC)
    - [基本設定](#%E5%9F%BA%E6%9C%AC%E8%A8%AD%E5%AE%9A)
    - [Simpleperf](#simpleperf)
    - [Benchmark](#benchmark)
    - [PMU Selection](#pmu-selection)

<!-- /TOC -->

---

### 計畫目標 
1. Performance model

    - 利用 ML Model 去預測手機的耗能與效能，且去預測何種Scheduling Policy可以達到更好的 效能與節能間的平衡。
2. FPSGO

    - CPU/GPU 在全速運作的情形下，會造成資源過剩/過熱的問題，希望能在省電的同時，還是能兼顧UI/遊戲的效能。

    - [notion 筆記連結](https://www.notion.so/FPSGO_study-2f4ae5a5651e452c91f51afc1ed14fe4)

### 設備規格
- Pixel 4/ Pixel 4XL

|            CPU            	|                          	|                           	|
|:-------------------------:	|:------------------------:	|:-------------------------:	|
| Qualcomm® Snapdragon™ 855 	|                          	|                           	|
| LITTLE cluster            	| big cluster              	| Prime cluster             	|
| 4x Kryo 485 Silver 1.8GHz 	| 3x Kryo 485 Gold 2.42GHz 	| 1x Kryo 485 Prime 2.84GHz 	|
| Cortex-A55                	| Cortex-A76               	| Cortex-A76                	|
| 6 PMU counters            	| 6 PMU counters           	| 6 PMU counters            	|

|                       	|      1 	|      2 	|       3 	|       4 	|       5 	|       6 	|       7 	|       8 	|       9 	|      10 	|      11 	|      12 	|      13 	|      14 	|      15 	|      16 	|      17 	|      18 	|      19 	|      20 	|
|-----------------------	|-------:	|-------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|
| Little Cluster (CPU0) 	| 300000 	| 403200 	|  499200 	|  576000 	|  672000 	|  768000 	|  844800 	|  940800 	| 1036800 	| 1113600 	| 1209600 	| 1305600 	| 1382400 	| 1478400 	| 1555200 	| 1632000 	| 1708800 	| 1785600 	|         	|         	|
| Medium Cluster (CPU4) 	| 710400 	| 825600 	|  940800 	| 1056000 	| 1171200 	| 1286400 	| 1401600 	| 1497600 	| 1612800 	| 1708800 	| 1804800 	| 1920000 	| 2016000 	| 2131200 	| 2227200 	| 2323200 	| 2419200 	|         	|         	|         	|
| Big Cluster (CPU7)    	| 825600 	| 940800 	| 1056000 	| 1171200 	| 1286400 	| 1401600 	| 1497600 	| 1612800 	| 1708800 	| 1804800 	| 1920000 	| 2016000 	| 2131200 	| 2227200 	| 2323200 	| 2419200 	| 2534400 	| 2649600 	| 2745600 	| 2841600 	|

### 基本設定

- 找頻率

```Shell
# 進到Android 手機的Shell
adb shell

# 知道CPU 的 所有Frequency (print)
cat "/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies"
cat "/sys/devices/system/cpu/cpu4/cpufreq/scaling_available_frequencies"
cat "/sys/devices/system/cpu/cpu7/cpufreq/scaling_available_frequencies"
```

- 定核


```
 基本介紹
num: xxxx xxxx
cpu: 7654 3210
```
1. 定核於cpu1(小核)
``` 
taskset 02 (0000 0010)
```
2. 定核於cpu5(中核) 
```
taskset 20 (0010 0000)
```
3. 定核於cpu7(大核) 
```
taskset 80 (1000 0000)
```

- 定頻
```sh
#調整上下限頻率後再做定頻這裡以小核為例,所以為policy0中核為policy4, 大核為policy7
adb shell "chmod 660 /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"
adb shell "chmod 660 /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq"
adb shell "echo 0 > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"
adb shell "echo 99999999 > /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq"
adb shell "echo sugov_ext > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor"
adb shell "echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor"
```
```sh
#定頻於 1800000 Hz (小核最高頻)
adb shell "chmod 660 /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"
adb shell "chmod 660 /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq"
adb shell "echo 1800000 > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"
adb shell "echo 1800000 > /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq"
adb shell "chmod 440 /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"
adb shell "chmod 440 /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq"
```

### Simpleperf

- 安裝
```
git clone https://android.googlesource.com/platform/prebuilts/simpleperf

#Find simpleperf 執行檔
cd E:\pixel\simpleperf\bin\android\arm64
adb push ./simpleperf [目的path]
```

- script
```
python3 profiler.py [-h] [-b BENCHMARK] [-o OUTPUTFILE]
```


<!-- ### Benchmark
- Mibench
    + 執行
    ```
    ```
    + [Data]()

- Lmbench
    + 執行
    ```
    ./bw_mem 512m [執行檔]
    ```
    + [Data]()

- Longbottom
    + [Source Code]() 
    + 執行
    + [Data]()

- Dhrystone
    + [Source Code]() 
    + 執行
    ```
    ./dry
    ```
    + [Data]() -->

### PMU Selection
- 作法一
    + 在高中低頻 大中小核，相關係數大於0.99的PMU
    + [Source Code](https://github.com/Essen-Lin/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/tree/master/src) 
    ```
    python3 PMU_select_freq.py
    ```
    + [Result](https://github.com/Essen-Lin/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/tree/master/src)
- 作法二
    + 分大中小核，把不同頻點一起考慮，相關係數大於0.9的PMU
    + [Source Code](https://github.com/Essen-Lin/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/tree/master/src) 
     ```
    python3 PMU_select_cluster.py
    ```
    + [Result](https://github.com/Essen-Lin/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/tree/master/src)
- 作法三(論文做法)
    + Hierarchical Clustering 分群+透過多次Linear Regression 篩選 PMU
    + [Source Code](https://github.com/Essen-Lin/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/tree/master/src) 
     ```
    python3 PMU_select_two_stage.py
    ```
    + [Result](https://github.com/Essen-Lin/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/tree/master/src)
- 作法四
    + 透過兩層filter篩選出PMU 並且生成Linear Regression Model
    + [Source Code](https://github.com/Essen-Lin/Performance-Prediction-and-Scheduling-on-Heterogeneous-CPUs/tree/master/src) 
     ```
    python3 PMU_select_filter.py
    ```

