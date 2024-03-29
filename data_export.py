import pandas as pd
import sys
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import argparse
import bz2

from ann_benchmarks.datasets import get_dataset
from ann_benchmarks.algorithms.definitions import get_definitions
from ann_benchmarks.plotting.metrics import all_metrics as metrics
from ann_benchmarks.plotting.utils  import get_plot_label, compute_metrics_all_runs, compute_metrics, create_linestyles, create_pointset
from ann_benchmarks.results import store_results, load_all_results, get_unique_algorithms

datasets = [
        'glove-100-angular',
        'sift-128-euclidean',
        'gist-960-euclidean',
        'random-10nn-euclidean',
        'nytimes-256-angular',
        'sift-256-hamming',
        'word2bits-800-hamming',
]

# datasets = [p[:-len('.hdf5')] for p in os.listdir('data') if p.endswith('.hdf5')]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--count',
        default=10)
    parser.add_argument(
        '--definitions',
        metavar='FILE',
        help='load algorithm definitions from FILE',
        default='algos.yaml')
    parser.add_argument(
        '--limit',
        default=-1)
    parser.add_argument(
        '--batch',
        help='Plot runs in batch mode',
        action='store_true')
    parser.add_argument(
        '--output',
        help='Path to the output csv file',
        required=True)
    parser.add_argument(
        '--recompute',
        action='store_true',
        help='Path to the output csv file')
    parser.add_argument(
        '--detail',
        action='store_true',
        help='Output the detailed information about each single query')
    args = parser.parse_args()

    count = int(args.count)
    dfs = []

    is_first = True
    pqwriter = None

    res = load_all_results()
    res_cnt = len(list(res))
    print("Found %d results, computing quality measures. This will take around %d minutes to process." % (res_cnt, res_cnt * 1.8 / 60))
    cnt = 0

    for dataset_name in datasets:
        for count in [10, 100]:
            for batch in [False, True]:
                #print("Loading results for dataset ", dataset_name, " with k=", count, " and batch=", batch, sep='')
                dataset = get_dataset(dataset_name)
                unique_algorithms = get_unique_algorithms()
                results = load_all_results(dataset_name, count, batch)
                results = compute_metrics_all_runs(dataset, results, args.recompute)
                df = pd.DataFrame(results)
                dfs.append(df)
                cnt += len(df)
                print("Inspected %d/%d results." % (cnt, res_cnt), end='\r')
    if len(dfs) > 0:
        data = pd.concat(dfs)
        data.to_csv(args.output, index=False)
    if pqwriter is not None:
        pqwriter.close()

