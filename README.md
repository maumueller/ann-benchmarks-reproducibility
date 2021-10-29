# Reproducibility Repository for ANN-Benchmarks: A benchmarking tool for approximate nearest neighbor search algorithms

This repository contains code to reproduce the experiments in 

>  M. Aumüller, E. Bernhardsson, A. Faithfull: [ANN-Benchmarks: A Benchmarking Tool for Approximate Nearest Neighbor Algorithms](https://arxiv.org/abs/1807.05614). Information Systems 2019. DOI: [10.1016/j.is.2019.02.006](https://doi.org/10.1016/j.is.2019.02.006) 

See <https://github.com/erikbern/ann-benchmarks> for the most recent state-of-art in nearest neighbor search.

## Reproduction

We provide here a detailed step-by-step discussion with explanations.
A summary of the different steps can be found in the bottom.

### Installation

There are two different ways to install the framework. You can either set up a VM ready to carry out the experiments using Vagrant, or you install the framework on your existing (Linux) setup.

#### Setting up a VM using Vagrant

We provide a `Vagrantfile` in the [research artifacts](https://doi.org/10.5281/zenodo.5613101)  that automatically sets up a VM ready to carry out the experiments.
See  <https://www.vagrantup.com/docs/installation> for how to install Vagrant using Virtualbox.

Next, download `Vagrantfile` and put it into a new directory. 
Edit `Vagrantfile` on line 51 and 52 to set up how many cpu cores and memory should be exposed to the VM.

Next, carry out the following steps in the directory where `Vagrantfile` resides.

```bash
vagrant up # sets up the vm
vagrant ssh  # connects to the machine
cd ann-benchmarks-reproducibility
```

Note that this setup does not allow to reproduce the (few) GPU runs mentioned in the paper, as detailed below.

#### Starting from an existing Linux environment

If the reproducibility framework is run in an existing linux installation,
we require that Python 3.6 or 3.8 and docker are installed. 
Starting from an Ubuntu 18.04 installation, the steps are as follows.

First, install docker. The necessary steps to carry out the installation are:

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update && sudo apt-get -y install apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
```
Afterwards, log out and back into your shell.

If an nvidia-GPU is present and the nvidia driver is installed, nvidia-docker can be installed as follows:
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

For the Python installation, in an Ubuntu 18.04 setup, Python 3.6 can be installed as follows:

```bash
sudo apt-get update 
sudo apt-get install -y python3-pip build-essential git
```

Next, clone the repository and install necessary dependencies and compile 
and install the nearest neighbor search implementations. 
The `--proc` flag specifies that the installation should use five processes in parallel.

```bash
git clone https://github.com/maumueller/ann-benchmarks-reproducibility
cd ann-benchmarks-reproducibility 
pip3 install -r requirements_py36.txt # use requirements_py38.txt for Python 3.8
python3 install.py --proc 5
```

For more recent versions of Python, the files `requirements_*.txt` has to be updated to contain recent versions of libraries. 
We provide a non-fixed version under `requirements.txt`.

Running CPU-based experiments
----------------------------

After setting up the Vagrant VM or finishing the installation in the local environment, we proceed to running the experiments.

Starting in the direction `ann-benchmarks-reproducibility`, we invoke all CPU-based experiments by running 
```bash
PY=python3 PARALLELISM=10 bash reproducibility/run_experiments.sh | tee -a runs.log
```
and write a log file to `runs.log`.

All individual runs of experiments in this part are carried out on a single CPU core using Docker. The environmental variable `PARALLELISM` can be used to spawn multiple containers in parallel. For a 10-core machine, we suggest using a value of 5.
The environmental variable `PY` can be used to point to a custom Python installation, e.g., provided by Anaconda.
Note that for the largest dataset `GIST-960-Euclidean`, around 20GB of RAM are necessary per process.
The environmental variable `GISTPARALLELISM` controls the number of parallel instances run for the GIST dataset. Invoking 

```bash
PY=python3 PARALLELISM=10 GISTPARALLELISM=3 bash reproducibility/run_experiments.sh | tee -a runs.log
```
corresponds to 3 parallel runs on GIST, and 10 on all other datasets. 
A machine used for running this experiment should contain at least 64GB of RAM.
On our test machine, reproducing all CPU based experiments with the parameters above took around 4 days.

Running GPU-based experiments
-----------------------------

The paper <https://arxiv.org/abs/1807.05614> contains a single run of a GPU-based variant in Figure 12. 
This run was carried out in a local environment outside a docker container.
To reproduce this run, we provide a script in `reproducibility/run_gpu.sh`. 
A Linux-based environment with a CUDA runtime of at least 10.2 is necessary.
This can be checked by inspecting the output of `nvidia-smi`.
Furthermore, the `nvidia-runtime` for docker must be installed, as detailed in <https://github.com/NVIDIA/nvidia-docker>.
If these requirements are met, the GPU run is reproduced by running:

```bash
python3 install.py --algorithm faissgpu 
bash reproducibility/run_gpu.sh
```

Our machine was equipped with a Quadro M4000 with compute engine 5.2 and all runs were finished within 10 minutes.
If the reproducibility environment features an older GPU, the version of the compute engine must be manually set during compilation of FAISS in `install/Dockerfile.faissgpu` by editing the flag `DCMAKE_CUDA_ARCHITECTURES="75;72;52"`.


Reproducing the Paper From The Results
======================================

If all runs above have been carried out, we can start reproducing the plots in the paper. 
Run

```bash
sudo python3 data_export --out res.csv
mkdir -p paper/result_tables/
python3 reproducibility/create_result_tables.py res.csv paper/result_tables/
python3 reproducibility/generate_and_verify_plots.py
```

to create all the raw tables used by `pgfplots` during the final LateX compilation.
Since exporting the results will compute all quality metrics, it took around 1 hour on our machine.
(However, results are cached, so this cost applies only once.)
The script `generate_and_verify_plots.py` will generate the plot tex files necessary to compile the document.
It will also list missing data points, e.g., because the computation timed out, a too old CPU architecture was used, or no GPU was present.
Now, compile the paper by changing to the `paper` directory and compiling `paper.tex`, i.e., 

```bash
cd paper  && latexmk -pdf paper.tex
```

This requires a standard latex installation for scientific writing. 
If such a system is not present, we provide another Docker container in `paper`. 
The reproducibility steps are then 

```bash
docker build . -t ann-benchmarks-reproducibility-latex 
docker run -it -v "$(pwd)"/:/app/:rw ann-benchmarks-reproducibility-latex:latest
```

from within the `paper` directory.
The compilation will fail (or miss certain plot lines) if some runs did not finish in time. 
The compilation log will contain the name of all runs that are missing, which allows to individually re-run some experiments, for example with longer timeouts.

The final PDF can be seen in `paper/paper.pdf` and the plots can be compared to the original paper <https://arxiv.org/abs/1807.05614>.

Reproduction from the original raw results
==========================================

To avoid rerunning all experiments, the raw result of the original runs can be accessed from the research artifacts <https://doi.org/10.5281/zenodo.5613101>.
It is required to complete the installation steps first.
Unpack the results into the `ann-benchmarks` folder, and run
the same steps as above. 

Related Publications
==================

The following publication details design principles behind the benchmarking framework: 

- M. Aumüller, E. Bernhardsson, A. Faithfull:
[ANN-Benchmarks: A Benchmarking Tool for Approximate Nearest Neighbor Algorithms](https://arxiv.org/abs/1807.05614). Information Systems 2019. DOI: [10.1016/j.is.2019.02.006](https://doi.org/10.1016/j.is.2019.02.006)
- M. Aumüller, E. Bernhardsson, A. Faithfull:
[Reproducibility Paper for ANN-Benchmarks: A Benchmarking Tool for Approximate Nearest Neighbor Algorithms](http://itu.dk/people/maau/additional/ann_benchmarks_reproducibility.pdf). 
- Research artifacts:  <https://doi.org/10.5281/zenodo.5613101>
