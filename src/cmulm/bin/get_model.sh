#!/bin/bash
# 1 is the training file
# 2 is the prefix for the model files

cat $1 | ./text2wfreq -hash 10000000 > $2.wfreq
cat $2.wfreq | ./wfreq2vocab -top 65000 -records 10000000 > $2.vocab
cat $1 | ./text2idngram -vocab $2.vocab -temp ./tmp/ -buffer 200 -fof_size 20 > $2.id3gram.bin
./idngram2lm -calc_mem -idngram $2.id3gram.bin -vocab $2.vocab -binary $2.binlm -bin_input -n 3
