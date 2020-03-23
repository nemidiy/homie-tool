[![tests](https://circleci.com/gh/nemidiy/homie-tool.svg?style=shield)](https://circleci.com/gh/nemidiy/homie-tool)

git config --local core.hooksPath .githooks/

docker image build -t homie-tool:0.2 .
docker container run --name ht homie-tool:0.2