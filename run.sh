# Mibench

## automotive
### bitcount
#python3 src/profiler.py -b "/data/local/tmp/Mibench/automotive/bitcount/bitcnts 84600000" -o "bin/Mibench/bitcnts/84600000.csv"

##consumer - fail

##network
python3 src/profiler.py -b "/data/local/tmp/Mibench/aarch64/network/dijkstra/dijkstra_small input.dat > output_small.dat" -o "/data/result/Mibench/dijkstra/dijkstra_small.csv"
python3 src/profiler.py -b "/data/local/tmp/Mibench/aarch64/network/dijkstra/dijkstra_large input.dat > output_large.dat" -o "/data/result/Mibench/dijkstra/dijkstra_large.csv"

# LMbench

# ## rd
# python3 src/profiler.py -b "/data/local/tmp/LMbench/bw_mem 512m rd" -o "bin/LMbench/bw_mem/512m/rd.csv"
# ## frd
# python3 src/profiler.py -b "/data/local/tmp/LMbench/bw_mem 512m frd" -o "bin/LMbench/bw_mem/512m/frd.csv"
# ## cp
# python3 src/profiler.py -b "/data/local/tmp/LMbench/bw_mem 512m cp" -o "bin/LMbench/bw_mem/512m/cp.csv"
# ## fcp
# python3 src/profiler.py -b "/data/local/tmp/LMbench/bw_mem 512m fcp" -o "bin/LMbench/bw_mem/512m/fcp.csv"
# ## bzero
# python3 src/profiler.py -b "/data/local/tmp/LMbench/bw_mem 512m bzero" -o "bin/LMbench/bw_mem/512m/bzero.csv"
# ## bcopy
# python3 src/profiler.py -b "/data/local/tmp/LMbench/bw_mem 512m bcopy" -o "bin/LMbench/bw_mem/512m/bcopy.csv"

# # Dhrystone
# python3 src/profiler.py -b "/data/local/tmp/Dhrystone/dry" -o "bin/Dhrystone/dry.csv"

# # SPEC CPU® 2017

# ## 600.perlbench_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/600.perlbench_s/run_base_test_mytest-64.0000/600.perlbench_s.sh" -o "bin/SpecCpu2017/600.perlbench_s.csv"
# ## 602.gcc_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/602.gcc_s/run_base_test_mytest-64.0000/602.gcc_s.sh" -o "bin/SpecCpu2017/602.gcc_s.csv"
# ## 605.mcf_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/605.mcf_s/run_base_test_mytest-64.0000/605.mcf_s.sh" -o "bin/SpecCpu2017/605.mcf_s.csv"
# ## 619.lbm_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/619.lbm_s/run_base_test_mytest-64.0000/619.lbm_s.sh" -o "bin/SpecCpu2017/619.lbm_s.csv"
# ## 620.omnetpp_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/620.omnetpp_s/run_base_test_mytest-64.0000/620.omnetpp_s.sh" -o "bin/SpecCpu2017/620.omnetpp_s.csv"
# ## 623.xalancbmk_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/623.xalancbmk_s/run_base_test_mytest-64.0000/623.xalancbmk_s.sh" -o "bin/SpecCpu2017/623.xalancbmk_s.csv"
# ## 625.x264_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/625.x264_s/run_base_test_mytest-64.0000/625.x264_s.sh" -o "bin/SpecCpu2017/625.x264_s.csv"
# ## 631.deepsjeng_s (Deprecated)
# ## python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/631.deepsjeng_s/run_base_test_mytest-64.0000/631.deepsjeng_s.sh" -o "bin/SpecCpu2017/631.deepsjeng_s.csv"
# ## 638.imagick_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/638.imagick_s/run_base_test_mytest-64.0000/638.imagick_s.sh" -o "bin/SpecCpu2017/638.imagick_s.csv"
# ## 641.leela_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/641.leela_s/run_base_test_mytest-64.0000/641.leela_s.sh" -o "bin/SpecCpu2017/641.leela_s.csv"
# ## 644.nab_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/644.nab_s/run_base_test_mytest-64.0000/644.nab_s.sh" -o "bin/SpecCpu2017/644.nab_s.csv"
# ## 657.xz_s
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2017/657.xz_s/run_base_test_mytest-64.0000/657.xz_s.sh" -o "bin/SpecCpu2017/657.xz_s.csv"

# # SPEC CPU® 2006

# ## 400.perlbench
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/400.perlbench/run_base_test_lnx64-gcc.0000/400.perlbench.sh" -o "bin/SpecCpu2006/400.perlbench.csv"
# ## 401.bzip2
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/401.bzip2/run_base_test_lnx64-gcc.0000/401.bzip2.sh" -o "bin/SpecCpu2006/401.bzip2.csv"
# ## 403.gcc
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/403.gcc/run_base_test_lnx64-gcc.0000/403.gcc.sh" -o "bin/SpecCpu2006/403.gcc.csv"
# ## 429.mcf
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/429.mcf/run_base_test_lnx64-gcc.0000/429.mcf.sh" -o "bin/SpecCpu2006/429.mcf.csv"
# ## 433.milc
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/433.milc/run_base_test_lnx64-gcc.0000/433.milc.sh" -o "bin/SpecCpu2006/433.milc.csv"
# ## 444.namd
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/444.namd/run_base_test_lnx64-gcc.0000/444.namd.sh" -o "bin/SpecCpu2006/444.namd.csv"
# ## 445.gobmk
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/445.gobmk/run_base_test_lnx64-gcc.0000/445.gobmk.sh" -o "bin/SpecCpu2006/445.gobmk.csv"
# ## 447.dealII
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/447.dealII/run_base_test_lnx64-gcc.0000/447.dealII.sh" -o "bin/SpecCpu2006/447.dealII.csv"
# ## 450.soplex
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/450.soplex/run_base_test_lnx64-gcc.0000/450.soplex.sh" -o "bin/SpecCpu2006/450.soplex.csv"
# ## 453.povray
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/453.povray/run_base_test_lnx64-gcc.0000/453.povray.sh" -o "bin/SpecCpu2006/453.povray.csv"
# ## 456.hmmer
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/456.hmmer/run_base_test_lnx64-gcc.0000/456.hmmer.sh" -o "bin/SpecCpu2006/456.hmmer.csv"
# ## 458.sjeng
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/458.sjeng/run_base_test_lnx64-gcc.0000/458.sjeng.sh" -o "bin/SpecCpu2006/458.sjeng.csv"
# ## 462.libquantum
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/462.libquantum/run_base_test_lnx64-gcc.0000/462.libquantum.sh" -o "bin/SpecCpu2006/462.libquantum.csv"
# ## 464.h264ref
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/464.h264ref/run_base_test_lnx64-gcc.0000/464.h264ref.sh" -o "bin/SpecCpu2006/464.h264ref.csv"
# ## 470.lbm
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/470.lbm/run_base_test_lnx64-gcc.0000/470.lbm.sh" -o "bin/SpecCpu2006/470.lbm.csv"
# ## 471.omnetpp
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/471.omnetpp/run_base_test_lnx64-gcc.0000/471.omnetpp.sh" -o "bin/SpecCpu2006/471.omnetpp.csv"
# ## 473.astar
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/473.astar/run_base_test_lnx64-gcc.0000/473.astar.sh" -o "bin/SpecCpu2006/473.astar.csv"
# ## 482.sphinx3
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/482.sphinx3/run_base_test_lnx64-gcc.0000/482.sphinx3.sh" -o "bin/SpecCpu2006/482.sphinx3.csv"
# ## 483.xalancbmk
# python3 src/profiler.py -b "/data/local/tmp/SpecCpu2006/483.xalancbmk/run_base_test_lnx64-gcc.0000/483.xalancbmk.sh" -o "bin/SpecCpu2006/483.xalancbmk.csv"
