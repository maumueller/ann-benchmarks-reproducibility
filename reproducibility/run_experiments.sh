PYTHON=${PY:="python3 -u"}
PARALLEL=${PARALLELISM:=1}
GISTPARALLEL=${GISTPARALLELISM:=$PARALLEL}

# K=10 runs
ALGODEF=reproducibility/standard_runs.yaml

start=`date +%s`
echo Started experiments at `date`

mkdir -p logs

for ds in glove-100-angular sift-128-euclidean random-10nn-euclidean; do
    $PYTHON run.py --dataset $ds --definition $ALGODEF --runs 3 --count 10 --parallelism $PARALLEL
    cp annb.log logs/${ds}_10.log
done

$PYTHON run.py --dataset glove-100-angular --runs 1 --count 10 --algorithm bruteforce-blas --definition $ALGODEF --run-disabled

$PYTHON run.py --dataset nytimes-256-angular --definition reproducibility/nytimes_runs.yaml --runs 3 --count 10 --parallelism $PARALLEL
cp annb.log logs/nytimes-256-angular_10.log


# K=100 runs
for ds in glove-100-angular sift-128-euclidean; do
    $PYTHON run.py --dataset $ds --definition $ALGODEF --runs 1 --count 100 --parallelism $PARALLEL
    cp annb.log logs/${ds}_100.log
done

# separate GIST runs because of high RAM usage

$PYTHON run.py --dataset gist-960-euclidean --definition $ALGODEF --runs 1 --count 10 --parallelism $GISTPARALLEL
cp annb.log logs/gist-960-euclidean_10.log
$PYTHON run.py --dataset gist-960-euclidean --definition $ALGODEF --runs 1 --count 100 --parallelism $GISTPARALLEL
cp annb.log logs/gist-960-euclidean_100.log


# Hamming
ALGODEF=reproducibility/hamming_runs.yaml
for ds in sift-256-hamming word2bits-800-hamming; do
    $PYTHON run.py --dataset $ds --definition $ALGODEF --runs 1 --count 10 --parallelism $PARALLEL
    cp annb.log logs/${ds}_10.log
done

# Batch runs without GPU
# see run_gpu.sh for running GPU experiment in Figure 12
ALGODEF=reproducibility/batch_runs.yaml
$PYTHON run.py --dataset sift-128-euclidean --definition $ALGODEF --batch --count 10
cp annb.log logs/sift-128-euclidean-batch_10.log

end=`date +%s`
echo Finished experiments at `date`

echo Spent $((end- start))s reproducing the experiments.



