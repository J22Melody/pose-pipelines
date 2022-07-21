FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install sudo git wget build-essential -y

# download and install the latest version of cmake
RUN wget -c "https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4.tar.gz"
RUN tar xf cmake-3.14.4.tar.gz
RUN cd cmake-3.14.4 && ./configure
RUN cd cmake-3.14.4 && make
RUN cd cmake-3.14.4 && make install

# download OpenPose from Git Repository
RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git

# Install OpenCV
ENV TZ=Europe/Minsk
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install libopencv-dev -y

# install dependencies
RUN chmod -R +x ./openpose/scripts/ubuntu/
RUN ./openpose/scripts/ubuntu/install_deps.sh
#RUN ./openpose/scripts/ubuntu/install_cuda.sh
#RUN ./openpose/scripts/ubuntu/install_cudnn.sh


# this is just a fix to address few compilation issues
RUN sed -i 's/execute_process(COMMAND git checkout master WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/execute_process(COMMAND git checkout f019d0dfe86f49d1140961f8c7dec22130c83154 WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/g' openpose/CMakeLists.txt
RUN cd openpose && git pull origin master

# compiling OpenPose with cmake
RUN cd openpose && mkdir build && cd build && cmake -DBUILD_PYTHON=ON ..
RUN cd openpose/build && make -j `nproc`
RUN cd openpose/models && ./getModels.sh

RUN pip3 install opencv-python flask Pillow

RUN mkdir /out

RUN mkdir workspace
WORKDIR workspace


COPY api/ api/
RUN chmod 777 -R api/


# nvidia-docker build -t "openpose" .
# python3 /workspace/api/server.py
# nvidia-docker run -it --rm  -p 8485:8485 -v /home/nlp/amit/pose/OpenPose/api:/workspace/api openpose python3 /workspace/api/server.py

# nvidia-docker run -it --rm -v /home/nlp/amit/pose/OpenPose/api:/workspace/api -v /home/nlp/amit/pose/assets:/workspace/assets -v /home/nlp/amit/pose/output:/workspace/out openpose

# wget http://www.handspeak.com/word/c/ceramic-fs.mp4


# python3 api/hand.py --input assets/hands --output out -f image

# ! cd openpose && ./build/examples/openpose/openpose.bin --video ../between.mp4  --display 0 --write_json out/ --hand --face --num_gpu 4 # --write_video /out.avi