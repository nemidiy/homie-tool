[![tests](https://circleci.com/gh/nemidiy/homie-tool.svg?style=shield)](https://circleci.com/gh/nemidiy/homie-tool)

git config --local core.hooksPath .githooks/

docker image build -t homie-tool:0.2 .
docker container run --name ht homie-tool:0.2
docker run -it a7d8e2f1fc55 bash
docker run -it a7d8e2f1fc55 test

docker pull eclipse-mosquitto
docker run -it eclipse-mosquitto sh

docker run -it -p 2883:2883 \
	-v $(pwd)/mosquitto.docker.conf:/mosquitto/config/mosquitto.conf \
	-v /mosquitto/data \
	-v /mosquitto/log \
	eclipse-mosquitto

