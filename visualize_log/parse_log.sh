#!/bin/bash
# Usage parse_log.sh caffe.log
# It creates the following two text files, each containing a table:
#     caffe.log.test (columns: '#Iters Seconds TestAccuracy TestLoss')
#     caffe.log.train (columns: '#Iters Seconds TrainingLoss LearningRate')


# get the dirname of the script
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

if [ "$#" -lt 1 ]
then
echo "Usage parse_log.sh /path/to/your.log"
exit
fi
LOG=`basename $1`
sed -n '/Iteration .* Testing net/,/Iteration *. loss/p' $1 > auxt.txt
sed -i '/Waiting for data/d' auxt.txt
sed -i '/prefetch queue empty/d' auxt.txt
sed -i '/Iteration .* loss/d' auxt.txt
sed -i '/Iteration .* lr/d' auxt.txt
sed -i '/Train net/d' auxt.txt
grep 'Iteration ' auxt.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > auxt0.txt
grep 'Test net output #0' auxt.txt | awk '{print $11}' > auxt1.txt
grep 'Test net output #1' auxt.txt | awk '{print $11}' > auxt2.txt

# Extracting elapsed seconds
# For extraction of time since this line contains the start time
grep '] Solving ' $1 > auxt3.txt
grep 'Testing net' $1 >> auxt3.txt
$DIR/extract_seconds.py auxt3.txt auxt4.txt

# Generating
echo '#Iters Seconds TestAccuracy TestLoss'> $LOG.test
paste auxt0.txt auxt4.txt auxt1.txt auxt2.txt | column -t >> $LOG.test
rm auxt.txt auxt0.txt auxt1.txt auxt2.txt auxt3.txt auxt4.txt

# For extraction of time since this line contains the start time
grep '] Solving ' $1 > auxt.txt
grep ', loss = ' $1 >> auxt.txt
grep 'Iteration ' auxt.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > auxt0.txt
grep ', loss = ' $1 | awk '{print $9}' > auxt1.txt
grep ', lr = ' $1 | awk '{print $9}' > auxt2.txt

# Extracting elapsed seconds
$DIR/extract_seconds.py auxt.txt auxt3.txt

# Generating
echo '#Iters Seconds TrainingLoss LearningRate'> $LOG.train
paste auxt0.txt auxt3.txt auxt1.txt auxt2.txt | column -t >> $LOG.train
rm auxt.txt auxt0.txt auxt1.txt auxt2.txt  auxt3.txt
