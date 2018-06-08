1. create a user defined network

all containers inside the network layer can talk to each other
*******************************************
docker network create chatbot
*******************************************

2. mongodb docker
this db is used to store data communicated between frontend(debtor) and server(chatbot)

docker pull mongo
docker run -d --name chatbotdb --network chatbot mongo

3. run cuda8-cu6 docker
docker run -it -d -u 1000  -v  ~/DockerDev/jupyter:/home/kai/data -p 8888-8890:8888-8890 --name pythonEnv --network chatbot toneymall/cuda8-cu6