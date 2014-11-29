#!/usr/bin/env sh

dir="./results"
rm -rf $dir
mkdir $dir

gcc -O3 -o ./markov ./markov.c

# Configuration de k
kMin=2
kMax=20
kStep=1

# Configuration de m
mMin=100000
mMax=1000000
mStep=100000

# Nombre d'exec par configuration
N=100

# Liste des textes
texts="don-quixote.txt madame-bovary.txt zadig.txt"

for txt in $texts; do
  n=$(cat $txt | wc -w)
  for k in $(seq $kMin $kStep $kMax); do
    for m in $(seq $mMin $mStep $mMax); do
      echo "$N executions avec k=$k, m=$m, n=$n, txt=$txt"
      for i in $(seq 1 $N); do
        /usr/local/bin/time -a -o "$dir/time-$txt-$k-$m-$n" -f "%e" \
          ./markov $k $m < $txt > /dev/null 2>> "$dir/count-$txt-$k-$m-$n"
      done
    done
  done
done
