docker run -it -d -u 1000 -v ~/DockerDev:/home/kai/data -p 8888-8890:8888-8890 -p 6006:6006 --name pythonEnv --network chatbot toneymall/cuda8-cu6


docker run -it -d -p 27017:27017 --name chatbotdb --network chatbot mongo
docker run -it -d  --name chatbotdb --network chatbot mongo



docker exec -it pythonEnv bash
cd /home/kai/data
jupyter notebook > notebook.log 2>&1 &








docker run -it -d -u 1000 -v ~/DockerDev/jupyter:/home/kai/data  --name cuda9 nvidia/cuda:9.2-cudnn7-devel

cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/local/cuda/lib64/libOpenCL.so.1.0.0 -DOpenCL_INCLUDE_DIR=/usr/local/cuda/include/ ..



docker run -it  --name cuda9 nvidia/cuda:9.2-cudnn7-devel
curl -O https://repo.continuum.io/archive/Anaconda3-5.2.0-Linux-x86_64.sh






You may wish to edit your .bashrc to prepend the Anaconda3 install location to PATH:

go to ~/.bashrc, add below to last line
export PATH=/home/kai/anaconda3/bin:$PATH

Then source ~/.bashrc

Thank you for installing Anaconda3!