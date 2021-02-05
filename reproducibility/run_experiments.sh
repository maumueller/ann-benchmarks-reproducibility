#for ds in glove-100-angular sift-128-euclidean random-10nn-euclidean gist-960-euclidean nytimes-256-angular sift-256-hamming word2bits-800-hamming; do
#    python3 create_dataset.py --dataset $ds
#done

python=/home/maau/miniconda3.6/bin/python

# K=10 runs
ALGODEF=reproducibility/standard_runs.yaml

mkdir -p logs

for ds in glove-100-angular sift-128-euclidean random-10nn-euclidean gist-960-euclidean nytimes-256-angular; do
    $python run.py --dataset $ds --definition $ALGODEF --runs 3 --count 10 --parallelism 20
    cp annb.log logs/${ds}_10.log
done


# K=100 runs
for ds in glove-100-angular sift-128-euclidean gist-960-euclidean; do
    $python run.py --dataset $ds --definition $ALGODEF --runs 1 --count 100 --parallelism 20
    cp annb.log logs/${ds}_100.log
done

# Hamming
ALGODEF=reproducibility/hamming_runs.yaml
for ds in sift-256-hamming word2bits-800-hamming; do
    $python run.py --dataset $ds --definition $ALGODEF --runs 1 --count 10 --parallelism 20
    cp annb.log logs/${ds}_10.log
done

# GPU
#ALGODEF=reproducibility/batch_runs.yaml
#python3 run.py --dataset sift-128-euclidean --definition $ALGODEF --batch --count 10 --local
#python run.py --dataset $ds --definition $ALGODEF --runs 1 --count 10 --local




