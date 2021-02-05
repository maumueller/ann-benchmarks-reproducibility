from math import ceil
import pandas as pd
import sys

def get_pareto_frontier(df, x, y, split, ascending=False):
    # removes all rows that don't lie on the pareto frontier
    to_plot = df.sort_values(y,ascending=ascending).reset_index(drop=True)
    d = {} # store last x values
    drop_list = []
    for algo in set(df[split]):
        d[algo] = 0
    for i in range(len(to_plot)):
        x_ = to_plot.iloc[i][x]
        y_ = to_plot.iloc[i][y]
        algo = to_plot.iloc[i][split]
        if x_ > d[algo]:
            d[algo] = x_
        else:
            drop_list.append(i)
    to_plot.drop(drop_list, inplace=True)

    return to_plot

df = pd.read_csv(sys.argv[1])
outputdir = sys.argv[2]

df['dslabel'] = df.apply(lambda row: row.dataset + str(row["count"]), axis = 1)
df['qps*buildtime'] = df.apply(lambda row: row.qps * row.build, axis = 1)

datasets = set(df.dataset)
algorithms = set(df.algorithm)

for dataset in datasets:
    for count in [10, 100]:
        for x_metric in ['k-nn', 'epsilon', 'largeepsilon']:
            for y_metric in ['qps', 'build', 'queriessize', 'qps*buildtime']:
                test_df = df[(df.dataset == dataset) & (df["count"] == count) & (df.batch == False)]
                test_df = get_pareto_frontier(test_df, x_metric, y_metric, "algorithm", y_metric == 'queriessize')
                for algorithm in set(test_df.algorithm):
                    fn = "%s_%d_%s_%s_%s" % (dataset, count, algorithm, x_metric, y_metric)
                    with open("%s/%s" % (outputdir, fn), 'w') as f:
                        for x, y in test_df[test_df.algorithm == algorithm][[x_metric, y_metric]].itertuples(index=False):
                            f.write("%f %f\n" % (x, y))

for dataset in datasets:
    for count in [10, 100]:
        for x_metric in ['k-nn', 'epsilon', 'largeepsilon']:
            for y_metric in ['qps', 'build', 'queriessize', 'qps*buildtime']:
                test_df = df[(df.dataset == dataset) & (df["count"] == count) & (df.batch == True)]
                test_df = get_pareto_frontier(test_df, x_metric, y_metric, "algorithm", y_metric == 'queriessize')
                for algorithm in set(test_df.algorithm):
                    fn = "%s_%d_%s-batch_%s_%s" % (dataset, count, algorithm, x_metric, y_metric)
                    with open("%s/%s" % (outputdir, fn), 'w') as f:
                        for x, y in test_df[test_df.algorithm == algorithm][[x_metric, y_metric]].itertuples(index=False):
                            f.write("%f %f\n" % (x, y))
algorithms = set(df.algorithm)

for algorithm in algorithms:
        for x_metric in ['k-nn', 'epsilon', 'largeepsilon']:
            for y_metric in ['qps', 'build', 'queriessize', 'qps*buildtime']:
                test_df = df[(df.algorithm == algorithm) & (df.batch == False)]
                test_df = get_pareto_frontier(test_df, x_metric, y_metric, "dslabel", y_metric == 'queriessize')
                for dataset in set(test_df.dataset):
                    for count in [10, 100]:
                        fn = "%s_%s_%d_%s_%s" % (algorithm, dataset, count, x_metric, y_metric)
                        with open("%s/%s" % (outputdir, fn), 'w') as f:
                            for x, y in test_df[(test_df.dataset == dataset) & (test_df["count"] == count)][[x_metric, y_metric]].itertuples(index=False):
                                f.write("%f %f\n" % (x, y))

for algorithm in algorithms:
        for x_metric in ['k-nn', 'epsilon', 'largeepsilon']:
            for y_metric in ['qps', 'build', 'queriessize', 'qps*buildtime']:
                test_df = df[(df.algorithm == algorithm) & (df.batch == True)]
                test_df = get_pareto_frontier(test_df, x_metric, y_metric, "dslabel", y_metric == 'queriessize')
                for dataset in set(test_df.dataset):
                    for count in [10, 100]:
                        fn = "%s-batch_%s_%d_%s_%s" % (algorithm, dataset, count, x_metric, y_metric)
                        with open("%s/%s" % (outputdir, fn), 'w') as f:
                            for x, y in test_df[(test_df.dataset == dataset) & (test_df["count"] == count)][[x_metric, y_metric]].itertuples(index=False):
                                f.write("%f %f\n" % (x, y))

# code to generate the tex code for the bar chart
# because it seems difficult to read the labels from the file with pgfplots
algos = {
    "faiss-ivf": "FAISS-IVF",
    "annoy" : "ANNOY",
    "BallTree(nmslib)" : "BALLTREE",
    "pynndescent" : "PyNNDescent",
    "SW-graph(nmslib)" : "SW-Graph",
    "hnsw(faiss)" : "HNSW(FAISS)",
    "rpforest": "RP-Forest",
    "NGT-onng" : "ONNG",
    "flann" : "FLANN",
    "kgraph" : "KGraph",
    "hnsw(nmslib)" : "HNSW(NMSlib)"
}

to_plot_algos = list(algos.keys())

result = []

for algo, time in df[(df.algorithm.isin(to_plot_algos)) & (df.dataset=="glove-100-angular") & (df["count"] == 10) & (df["k-nn"] >= 0.9)][['algorithm', 'build']].groupby(['algorithm']).min().sort_values(by="build").itertuples():
    result.append((algos[algo], ceil(time)))

with open("%s/build_bar.tex" % outputdir, "w") as f:
    f.write(r"""
\begin{figure}[t!]
\begin{tikzpicture}
\selectcolormodel{gray}
  \begin{axis}[
    ybar,
    enlargelimits=0.15,
    legend style={at={(0.5,-0.2)},
      anchor=north,legend columns=-1},
    ylabel={Build time (s)},
    width = .9\textwidth,
    height= 5.5cm,
    xtick=data,
    symbolic x coords = {
    %s
    },
    nodes near coords,
    nodes near coords align={vertical},
    x tick label style={rotate=45,anchor=east},
    ]
    \addplot coordinates {
    %s
    };
  \end{axis}
\end{tikzpicture}
\caption{Index build time in seconds for dataset \textsf{GLOVE}. The plot shows the minimum build time for an index that achieved recall of at least 0.9 for 10-NN.}
\label{fig:buildtime}
\end{figure}
""" % ((",%\n".join([x[0] for x in result])),
      (("\n".join(["(%s, %d)" % (x) for x in result])))))

# special code to produce the scatter plot for fig. 13

test_df = df[(df.dataset=="glove-100-angular") & (df["count"] == 10) & (df.algorithm.isin(["annoy", "faiss-ivf", "hnsw(nmslib)", "SW-graph(nmslib)"]))]
x_metric = "k-nn"
y_metric = "qps"
for algorithm in set(test_df.algorithm):
    fn = "%s_%d_%s_%s_%s" % ("glove-100-angular", 10, algorithm, x_metric, y_metric)
    with open("%s/scatter_%s" % (outputdir, fn), 'w') as f:
        for x, y in test_df[test_df.algorithm == algorithm][[x_metric, y_metric]].itertuples(index=False):
            f.write("%f %f\n" % (x, y))
