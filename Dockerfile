from ubuntu:18.04

# docker shouldn't be needed with current approach
RUN apt-get update
RUN apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update
RUN apt-get install -y docker-ce docker-ce-cli containerd.io
RUN	apt-get update -y && apt-get install -y ruby git python3-pip python3-dev build-essential wget 
RUN mkdir app 
WORKDIR /app

# TODO copy locally
RUN git clone https://github.com/maumueller/ann-benchmarks-reproducibility #
WORKDIR /app/ann-benchmarks-reproducibility
RUN pip3 install -r requirements.txt

#annoy

RUN git clone https://github.com/spotify/annoy
RUN cd annoy && git checkout 94988766fcfcb52114fb5e2deba9dca829f01db4 && python3 setup.py install
RUN python3 -c 'import annoy'

#faiss

RUN apt-get update && apt-get install -y libopenblas-base libopenblas-dev libpython-dev python-numpy python-pip swig
RUN git clone https://github.com/facebookresearch/faiss lib-faiss
RUN cd lib-faiss && git checkout e57270600a49fea2f7e86a7214755c4721be6602 && ./configure --without-cuda && make && make install && make py  
ENV PYTHONPATH lib-faiss/python/

# faiss doesn't work with python3 afaik
RUN python -c 'import faiss'
RUN pip install -rrequirements.txt
RUN pip install -r requirements.txt
RUN pip install sklearn enum34

# flann
RUN apt-get update && apt-get install -y cmake pkg-config liblz4-dev
RUN git clone https://github.com/mariusmuja/flann && cd flann && git checkout f3a17cd3f94a0e9dd8f6a55bce11536c50d4fb24
RUN mkdir flann/build
RUN cd flann/build && cmake ..
RUN cd flann/build && make -j4
RUN cd flann/build && make install
RUN pip install sklearn
RUN python -c 'import pyflann'

# kgraph
RUN apt-get update && apt-get install -y libboost-timer-dev libboost-chrono-dev libboost-program-options-dev libboost-system-dev libboost-python-dev
RUN git clone https://github.com/aaalgo/kgraph 
RUN cd kgraph && git checkout 4c517e5401dddab5f94219c41b7c5792fae810e8 && python3 setup.py build && python3 setup.py install
RUN python3 -c 'import pykgraph'

# mih 
RUN apt-get update && apt-get install -y cmake libhdf5-dev
RUN git clone https://github.com/maumueller/mih
RUN cd mih && git checkout d429e9b71c558593402ba6767da8496e8427d349 && mkdir bin && cd bin && cmake ../ && make -j4

# onng
RUN apt-get install -y git cmake g++ python3 python3-setuptools python3-pip
RUN pip3 install pybind11==2.2.4
RUN git clone https://github.com/yahoojapan/ngt.git && cd ngt && git checkout 9acca3dd48914f96fa4a5e63f6d426661460f7cc
RUN mkdir -p ngt/build
RUN cd ngt/build && cmake ..
RUN cd ngt/build && make && make install
RUN ldconfig
RUN cd ngt/python && python3 setup.py bdist_wheel
RUN pip3 install ngt/python/dist/ngt-*-linux_x86_64.whl


# nmslib
RUN apt-get update && apt-get install -y cmake libboost-all-dev libeigen3-dev libgsl0-dev
RUN git clone https://github.com/searchivarius/nmslib.git && cd nmslib && git checkout cd79cffafbcd60727510cd610ed4adb96301f5b4 
RUN cd nmslib/similarity_search && cmake . -DWITH_EXTRAS=1 
RUN cd nmslib/similarity_search && make -j4
RUN pip3 install pybind11
RUN cd nmslib/python_bindings && python3 setup.py build
RUN cd nmslib/python_bindings && python3 setup.py install
RUN python3 -c 'import nmslib'

# pynndescent 
RUN pip3 install 'numba==0.46' 'llvmlite==0.30' scikit-learn
RUN pip3 install 'pynndescent==0.2.1'
RUN python3 -c 'import pynndescent'

# rpforest
RUN git clone https://github.com/lyst/rpforest
RUN cd rpforest && git checkout a12ce33118b5267fcebe67ed817badb5e4682a7e && python3 setup.py install
RUN python3 -c 'import rpforest'
