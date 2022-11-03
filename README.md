## MTK 產學合作計畫 
<!-- vim-markdown-toc GFM -->
* [Goal](#計畫目標)
    - [Performance Model](#P)
    - [FPSGO](#FPSGO)
        
<!-- vim-markdown-toc -->

---

### 計畫目標 
1. Performance model

    - 利用 ML Model 去預測手機的耗能與效能，且去預測何種Scheduling Policy可以達到更好的 效能與節能間的平衡。
2. FPSGO

    - CPU/GPU 在全速運作的情形下，會造成資源過剩/過熱的問題，希望能在省電的同時，還是能兼顧UI/遊戲的效能。

    - [notion 筆記連結](https://www.notion.so/FPSGO_study-2f4ae5a5651e452c91f51afc1ed14fe4)

### 設備規格 Pixel Phone
- Pixel 4/ Pixel 4XL

|            CPU            	|                          	|                           	|
|:-------------------------:	|:------------------------:	|:-------------------------:	|
| Qualcomm® Snapdragon™ 855 	|                          	|                           	|
| LITTLE cluster            	| big cluster              	| Prime cluster             	|
| 4x Kryo 485 Silver 1.8GHz 	| 3x Kryo 485 Gold 2.42GHz 	| 1x Kryo 485 Prime 2.84GHz 	|
| Cortex-A55                	| Cortex-A76               	| Cortex-A76                	|
| 6 PMU counters            	| 6 PMU counters           	| 6 PMU counters            	|

### Frequency List

- How to find frequency
```Shell
# 進到Android 手機的Shell
adb shell

# 知道CPU 的 所有Frequency (print)
cat "/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies"
cat "/sys/devices/system/cpu/cpu4/cpufreq/scaling_available_frequencies"
cat "/sys/devices/system/cpu/cpu7/cpufreq/scaling_available_frequencies"
```
- Pixel 4XL Frequency List

|                       	|      1 	|      2 	|       3 	|       4 	|       5 	|       6 	|       7 	|       8 	|       9 	|      10 	|      11 	|      12 	|      13 	|      14 	|      15 	|      16 	|      17 	|      18 	|      19 	|      20 	|
|-----------------------	|-------:	|-------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|--------:	|
| Little Cluster (CPU0) 	| 300000 	| 403200 	|  499200 	|  576000 	|  672000 	|  768000 	|  844800 	|  940800 	| 1036800 	| 1113600 	| 1209600 	| 1305600 	| 1382400 	| 1478400 	| 1555200 	| 1632000 	| 1708800 	| 1785600 	|         	|         	|
| Medium Cluster (CPU4) 	| 710400 	| 825600 	|  940800 	| 1056000 	| 1171200 	| 1286400 	| 1401600 	| 1497600 	| 1612800 	| 1708800 	| 1804800 	| 1920000 	| 2016000 	| 2131200 	| 2227200 	| 2323200 	| 2419200 	|         	|         	|         	|
| Big Cluster (CPU7)    	| 825600 	| 940800 	| 1056000 	| 1171200 	| 1286400 	| 1401600 	| 1497600 	| 1612800 	| 1708800 	| 1804800 	| 1920000 	| 2016000 	| 2131200 	| 2227200 	| 2323200 	| 2419200 	| 2534400 	| 2649600 	| 2745600 	| 2841600 	|