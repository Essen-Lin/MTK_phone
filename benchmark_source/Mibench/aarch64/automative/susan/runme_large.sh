#!/bin/sh
/data/test/Mibench/susan/susan /data/test/Mibench/susan/input_large.pgm output_large.smoothing.pgm -s
/data/test/Mibench/susan/susan /data/test/Mibench/susan/input_large.pgm output_large.edges.pgm -e
/data/test/Mibench/susan/susan /data/test/Mibench/susan/input_large.pgm output_large.corners.pgm -c

