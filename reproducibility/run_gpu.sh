docker run --gpus all -v "$(pwd)"/ann_benchmarks:/home/app/ann_benchmarks:ro -v "$(pwd)"/data:/home/app/data:ro -v "$(pwd)"/results:/home/app/results:rw ann-benchmarks-faissgpu --dataset sift-128-euclidean --algorithm faiss-ivf-gpu --module ann_benchmarks.algorithms.faiss_gpu --constructor FaissGPUBF --runs 5 --count 10 --batch []

for centroids in 2048 4096 16384;
do for num_points in 1 20 50 100 200;
do
    docker run --gpus all -v "$(pwd)"/ann_benchmarks:/home/app/ann_benchmarks:ro -v "$(pwd)"/data:/home/app/data:ro -v "$(pwd)"/results:/home/app/results:rw ann-benchmarks-faissgpu --dataset sift-128-euclidean --algorithm faiss-ivf-gpu --module ann_benchmarks.algorithms.faiss_gpu --constructor FaissGPU --runs 5 --count 10 --batch  [$centroids,$num_points]
done;
done

