#! /usr/bin/env python3

import argparse
import csv
import logging
import re
import subprocess
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s line:%(lineno)-3d %(levelname)-8s ] %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)


class Profiler(object):

    def __init__(self) -> None:
        pass

    def profile(self, benchmark, outputfile):
        governors = (subprocess.run(["adb", "shell", "cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_governors"],
                                    stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines())[0].split()

        logging.info("available governors: ")
        logging.info("\t" + " ".join(governors))
        logging.info("")

        ###

        policies = subprocess.run(["adb", "shell", "ls /sys/devices/system/cpu/cpufreq"], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()

        logging.info("available clusters corresponding to policies: ")
        for i in range(len(policies)):
            logging.info("\tcluster" + str(i) + ", " + policies[i])
        logging.info("")

        ###

        frequencies = [
            i.split() for i in list(
                sorted(
                    set([
                        j for j in subprocess.run(["adb", "shell", "cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies"],
                                                  stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()
                    ])))
        ]

        for i in range(len(frequencies)):
            logging.info("available frequencies corresponding to " + policies[i] + ": ")
            logging.info("\t" + " ".join(frequencies[i]))
            logging.info("")

        ###

        raws = subprocess.run(["adb", "shell", "simpleperf", "list", "raw", "|", "grep", "raw-", "|", "awk", "'{print $1}'"],
                              stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()

        logging.info("available device pmu counters: ")
        for i in range(0, len(raws), 6):
            logging.info("\t" + ", ".join(raws[i:i + 6]))
        logging.info("")

        ###

        simpleperf = "simpleperf stat --use-devfreq-counters --per-core"

        logging.info("set simpleperf: ")
        logging.info("\t" + simpleperf)
        logging.info("")

        ###

        cwd = "cd " + str(Path(benchmark).parent)
        bin = "./" + Path(benchmark).name

        logging.info("set benchmark: ")
        logging.info("\t" + benchmark)
        logging.info("\t" + cwd)
        logging.info("\t" + bin)

        ###

        logging.info("")
        logging.info("set outputfile: ")
        logging.info("\t" + outputfile)
        logging.info("")

        ###

        sheet = [["setup core", "runtime core", "frequency", "coverage", "event", "count", "time"]]

        logging.info("set sheet titles: ")
        logging.info("\t" + " ".join(sheet[0]))
        logging.info("")

        ###

        governor = governors[2]

        logging.info("set governor policy: ")
        logging.info("\t" + governor)
        logging.info("")

        ###

        for idx in range(len(policies)):
            core = re.findall(r'\d+', policies[idx])[0]
            mask = format(1 << int(core), "02x")
            taskset = "taskset " + mask

            logging.info("set cluster corresponding to policy: ")
            logging.info("\tcluster" + str(idx) + ", " + policies[idx])
            logging.info("")
            logging.info("set core: ")
            logging.info("\tcore" + core)
            logging.info("")
            logging.info("set mask: ")
            logging.info("\t" + mask)
            logging.info("")
            logging.info("set taskset: ")
            logging.info("\t" + taskset)
            logging.info("")

            ###

            for frequency in [frequencies[idx][0], frequencies[idx][int((len(frequencies[idx]) - 1) / 2)], frequencies[idx][-1]]:
                subprocess.run(["adb", "shell", "echo 0 > /sys/devices/system/cpu/cpufreq/" + policies[idx] + "/scaling_min_freq"])
                subprocess.run(["adb", "shell", "echo 99999999 > /sys/devices/system/cpu/cpufreq/" + policies[idx] + "/scaling_max_freq"])
                subprocess.run(["adb", "shell", "echo " + governor + " > /sys/devices/system/cpu/cpufreq/" + policies[idx] + "/scaling_governor"])

                logging.info("set frequency: ")
                logging.info("\t" + frequency)
                logging.info("")

                ###

                subprocess.run(["adb", "shell", "echo " + frequency + " > /sys/devices/system/cpu/cpufreq/" + policies[idx] + "/scaling_min_freq"])

                logging.info("set min frequencies corresponding to cores: ")
                for i, minFreqency in enumerate(
                        subprocess.run(["adb", "shell", "cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq"],
                                       stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()):
                    logging.info("\t" + minFreqency.ljust(10, " ") + ", core" + str(i))
                logging.info("")

                ###

                subprocess.run(["adb", "shell", "echo " + frequency + " > /sys/devices/system/cpu/cpufreq/" + policies[idx] + "/scaling_max_freq"])

                logging.info("set max frequencies corresponding to cores: ")
                for i, maxFreqency in enumerate(
                        subprocess.run(["adb", "shell", "cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq"],
                                       stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()):
                    logging.info("\t" + maxFreqency.ljust(10, " ") + ", core" + str(i))
                logging.info("")

                ###

                logging.info("set cur frequencies corresponding to cores: ")
                for i, curFreqency in enumerate(
                        subprocess.run(["adb", "shell", "cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq"],
                                       stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()):
                    logging.info("\t" + curFreqency.ljust(10, " ") + ", core" + str(i))
                logging.info("")

                ###

                for i in range(0, len(raws), 6):
                    pmus = ",".join(raws[i:i + 6])

                    cmd = cwd + " && " + taskset + " " + simpleperf + " -e " + pmus + " " + bin

                    logging.info("run command: ")
                    logging.info("\t" + cmd)
                    print("")

                    ###

                    datas = [
                        j for j in [k.split() for k in filter(None,
                                                              subprocess.run(["adb", "shell", cmd], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines())]
                        if (len(j) and ((j[0] == core and j[-1] == "(100%)") or j[0] == 'Total'))
                    ]

                    for j in range(0, len(datas)):
                        if datas[j][0] == core:
                            sheet.append([core, datas[j][0], frequency, datas[j][-1].replace("(", "").replace(")", ""), datas[j][2], datas[j][1], datas[-1][3]])

                    print("")
                    for line in sheet:
                        for item in line:
                            print(item.ljust(27, " "), end="")
                        print("")
                    print("")

                    ###

        Path(outputfile).parent.mkdir(parents=True, exist_ok=True)

        logging.info("set output directory: ")
        logging.info(Path(outputfile).parent)
        logging.info("")

        with open(outputfile, "w") as f:
            w = csv.writer(f, dialect='excel')

            w.writerows(sheet)

        logging.info("set output file: ")
        logging.info(outputfile)


def main(argv):
    profiler = Profiler()

    profiler.profile(argv.benchmark[0], argv.outputfile[0])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    group = parser.add_argument_group()

    group.add_argument("-b", "--benchmark", nargs=1, type=str, help="string of benchmark command")
    group.add_argument("-o", "--outputfile", nargs=1, type=str, help="string of path to csv file")

    argv = parser.parse_args()

    if not argv.benchmark or not argv.outputfile:
        parser.error("Should have both benchmark and outputfile")

    main(argv)
