#!/bin/sh

# provide the path to the fastq files

indir=$1"*.fastq"
mkdir results_pear

R1s=(`ls $indir | grep "R1"`);
R2s=(`ls $indir | grep "R2"`);

for ((i=0;$i < ${#R1s[*]};i++ ));
        do
        outname=$(echo ${R1s[i]} | cut -d. -f1 | sed s"/_R1//")
        echo "Running :" $outname
        pear -f ${R1s[$i]} -r ${R2s[$i]} -o $outname -v 100 -j 20  -s 2 /dev/null >msg
        echo "Running :" $outname >> pearalignment.log
        grep -w "^Assembled reads " msg -A 2 >>pearalignment.log
        rm msg
done;

rm $1"/"*.discarded.*
rm $1"/"*.unassembled.*

mv $1"/"*.assembled.* pearalignment.log results_pear

echo "Done."
