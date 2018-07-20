docker run -it -d -u 1000 -v ~/DockerDev:/home/kai/data -p 8888-8890:8888-8890 -p 6006:6006 --name pythonEnv --network chatbot toneymall/cuda8-cu6


docker run -it -d -p 27017:27017 --name chatbotdb --network chatbot mongo
docker run -it -d  --name chatbotdb --network chatbot mongo



docker exec -it pythonEnv bash
cd /home/kai/data
jupyter notebook > notebook.log 2>&1 &