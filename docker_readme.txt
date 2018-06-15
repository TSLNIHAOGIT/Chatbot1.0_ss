docker run -it -d -u 1000 -v ~/DockerDev:/home/kai/data -p 8888-8890:8888-8890 -p 6006:6006 --name pythonEnv --network chatbot toneymall/cuda8-cu6

docker run -it -d --name chatbotdb --network chatbot mongo
